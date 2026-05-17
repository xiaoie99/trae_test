#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！
import requests
import base64
import os
_no_proxy = os.environ.get('no_proxy', os.environ.get('NO_PROXY', ''))
if 'fastapi.netdevops.com' not in _no_proxy:
    _no_proxy = (_no_proxy + ',fastapi.netdevops.com').strip(',')
    os.environ['no_proxy'] = os.environ['NO_PROXY'] = _no_proxy
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CA_CERT = os.path.join(SCRIPT_DIR, 'ca.crt')
server_ip = 'fastapi.netdevops.com'
base_url = f'https://{server_ip}/'
exec_cmd_url = base_url + 'cmd'
def json_rpc_client_exec_cmd(obj):
    return_json = requests.post(exec_cmd_url, json=obj, verify=CA_CERT).json()
    if return_json.get('cmd_result'):
        return base64.b64decode(return_json.get('cmd_result')).decode('utf-8')
    else:
        return base64.b64decode(return_json.get('error')).decode('utf-8')
if __name__ == "__main__":
    exec_cmd = {'cmd': 'ifconfig'}
    print(json_rpc_client_exec_cmd(exec_cmd))
    exec_cmd = {'cmd': 'ipconfig'}
    print(json_rpc_client_exec_cmd(exec_cmd))
