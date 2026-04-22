#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Tuple
from pymongo import MongoClient

MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb')
MONGO_PORT = int(os.environ.get('MONGO_PORT', '27017'))
MONGO_DB = os.environ.get('MONGO_DB', 'netflowdb')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', 'flows')


def get_mongo() -> Tuple[MongoClient, str, str]:
	"""Return Mongo client, database name, and collection name."""
	client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
	return client, MONGO_DB, MONGO_COLLECTION
