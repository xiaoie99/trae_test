#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import socketserver
import threading
import queue
import signal
import sys
from datetime import datetime, timezone
from typing import Dict, Optional

from pymongo import MongoClient, WriteConcern
from pymongo.collection import Collection

from netflow_parser_v9 import ExportPacket, TemplateRecord


# ------------ Config via env ------------
HOST = os.environ.get('NETFLOW_HOST', '0.0.0.0')
PORT = int(os.environ.get('NETFLOW_PORT', '2055'))
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb')
MONGO_PORT = int(os.environ.get('MONGO_PORT', '27017'))
MONGO_DB = os.environ.get('MONGO_DB', 'netflowdb')
MONGO_COLL = os.environ.get('MONGO_COLLECTION', 'flows')

BULK_SIZE = int(os.environ.get('BULK_SIZE', '500'))           # flush when >= N docs
FLUSH_MS = int(os.environ.get('FLUSH_MS', '200'))              # flush when >= T ms
WRITE_CONCERN = int(os.environ.get('WRITE_CONCERN', '1'))      # 1 or 0
REUSEPORT = os.environ.get('REUSEPORT', '1') == '1'            # enable SO_REUSEPORT


# ------------ Global state ------------
client: Optional[MongoClient] = None
collection: Optional[Collection] = None
stop_event = threading.Event()
write_queue: "queue.Queue[dict]" = queue.Queue(maxsize=10000)


def init_mongo() -> None:
	global client, collection
	wc = WriteConcern(WRITE_CONCERN)
	client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, w=WRITE_CONCERN)
	collection = client[MONGO_DB].get_collection(MONGO_COLL).with_options(write_concern=wc)
	print(f"Mongo connected {MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}.{MONGO_COLL} w={WRITE_CONCERN}")


def close_mongo() -> None:
	global client
	if client is not None:
		client.close()
		client = None


def writer_thread_fn() -> None:
	"""Background writer that flushes by size or time."""
	batch: list = []
	while not stop_event.is_set():
		try:
			item = write_queue.get(timeout=FLUSH_MS / 1000.0)
			batch.append(item)
			if len(batch) >= BULK_SIZE:
				flush_batch(batch)
				batch.clear()
		except queue.Empty:
			if batch:
				flush_batch(batch)
				batch.clear()
	# final flush
	if batch:
		flush_batch(batch)


def flush_batch(batch: list) -> None:
	if not batch:
		return
	assert collection is not None
	try:
		collection.insert_many(batch, ordered=False)
	except Exception as e:
		print(f"insert_many error: {e}")


class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
	allow_reuse_address = True
	def server_bind(self) -> None:
		if REUSEPORT and hasattr(socket, 'SO_REUSEPORT'):
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		super().server_bind()


class NetflowUDPHandler(socketserver.BaseRequestHandler):
	TEMPLATES: Dict[int, TemplateRecord] = {}

	@classmethod
	def get_server(cls, host: str, port: int):
		print(f"Listening on {host}:{port} (UDP, threading={True}, reuseport={REUSEPORT})")
		server = ThreadingUDPServer((host, port), cls)
		return server

	def handle(self):
		data = self.request[0]
		addr = self.client_address[0]
		export = ExportPacket(data, self.TEMPLATES)
		self.TEMPLATES.update(export.templates)

		if export.version != 9 or not export.flows:
			return

		utc_now = datetime.now(timezone.utc)
		for f in export.flows:
			doc = {
				'source_id': export.source_id,
				'sequence': export.sequence,
				'collector_received_at': utc_now,
				'fields': f,
			}
			try:
				write_queue.put(doc, timeout=0.05)
			except queue.Full:
				# drop when overwhelmed
				pass


server: Optional[ThreadingUDPServer] = None
writer_thread: Optional[threading.Thread] = None


def shutdown_handler(signum, frame):
	print('Shutting down...')
	stop_event.set()
	if server:
		server.shutdown()
		server.server_close()
	if writer_thread and writer_thread.is_alive():
		writer_thread.join(timeout=2)
	close_mongo()
	sys.exit(0)


if __name__ == '__main__':
	init_mongo()
	writer_thread = threading.Thread(target=writer_thread_fn, daemon=True)
	writer_thread.start()

	signal.signal(signal.SIGTERM, shutdown_handler)
	signal.signal(signal.SIGINT, shutdown_handler)

	server = NetflowUDPHandler.get_server(HOST, PORT)
	try:
		server.serve_forever(poll_interval=0.5)
	except KeyboardInterrupt:
		shutdown_handler(None, None)
