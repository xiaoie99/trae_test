#!/usr/bin/env python3
# -*- coding=utf-8 -*-
"""Day 10 - 使用 PyShark 解析 PCAP 并写入 Elasticsearch"""
import json
from datetime import timedelta
from datetime import timezone
from pathlib import Path
from urllib import error
from urllib import request
import pyshark
TZUTC_0 = timezone(timedelta(hours=0))
CURRENT_DIR = Path(__file__).resolve().parent
PCAP_FILE = CURRENT_DIR / 'pkt.pcap'
ES_URL = 'http://127.0.0.1:9200'
INDEX_NAME = 'qyt-pyshark-index'
def es_request(method, path, payload=None):
    """通过 Elasticsearch HTTP API 发送请求。"""
    data = None
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
    req = request.Request(
        f'{ES_URL}{path}',
        data=data,
        headers={'Content-Type': 'application/json'},
        method=method,
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except error.HTTPError as http_error:
        error_body = http_error.read().decode('utf-8', errors='ignore')
        raise RuntimeError(f'Elasticsearch 请求失败: {http_error.code} {error_body}') from http_error
def get_layer_fields(layer):
    """提取单个协议层的字段字典。"""
    layer_fields = getattr(layer, '_all_fields', {})
    if isinstance(layer_fields, dict):
        return layer_fields
    return {}
def normalize_packet(pkt):
    """把单个数据包整理为适合写入 Elasticsearch 的字典。"""
    pkt_dict = {}
    for layer in pkt.layers:
        pkt_dict.update(get_layer_fields(layer))
    pkt_dict_final = {}
    for k, v in pkt_dict.items():
        if k is None:
            continue
        ks = str(k).strip()
        if not ks:
            continue
        if v is None:
            continue
        if isinstance(v, str) and v.strip() == '':
            continue
        nk = ks.replace('.', '_')
        if not nk:
            continue
        if isinstance(v, (dict, list)):
            pkt_dict_final[nk] = json.dumps(v, ensure_ascii=False)
        elif isinstance(v, (str, int, float, bool)):
            pkt_dict_final[nk] = v
        else:
            pkt_dict_final[nk] = str(v)
    pkt_dict_final['sniff_time'] = pkt.sniff_time.astimezone(TZUTC_0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    pkt_dict_final['highest_layer'] = pkt.highest_layer
    ip_len = pkt_dict_final.get('ip_len')
    if ip_len is not None:
        try:
            pkt_dict_final['ip_len'] = int(ip_len)
        except (TypeError, ValueError):
            pass
    return {k: v for k, v in pkt_dict_final.items() if k}
def process_pcap():
    """读取 PCAP 文件并写入 Elasticsearch。"""
    cap = pyshark.FileCapture(str(PCAP_FILE), keep_packets=False)
    success_count = 0
    try:
        for packet_id, pkt in enumerate(cap, start=1):
            packet_data = normalize_packet(pkt)
            resp = es_request('POST', f'/{INDEX_NAME}/_doc', packet_data)
            print(resp.get('result', 'ok'))
            success_count += 1
    finally:
        cap.close()
    return success_count
if __name__ == '__main__':
    root = es_request('GET', '/')
    ver = root.get('version', {}).get('number', '?')
    print(f'[+] Elasticsearch 版本: {ver}')
    total_written = process_pcap()
    print(f'[+] 共写入 {total_written} 个数据包到 {INDEX_NAME}')
    cnt_body = es_request('GET', f'/{INDEX_NAME}/_count')
    doc_total = cnt_body.get('count', 0)
    print(f'[+] 当前索引文档总数: {doc_total}')
