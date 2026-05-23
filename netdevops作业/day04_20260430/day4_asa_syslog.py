#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 乾颐堂NetDevOps第四天作业：ASA REST API 配置 Syslog Server
import os
import ssl
ASA_ADDRESS = "10.10.1.98"
# 本机已设 http_proxy/https_proxy，需把 ASA 加入 no_proxy 直连，否则请求会走代理连不上防火墙；
_no_proxy = os.environ.get('no_proxy', os.environ.get('NO_PROXY', ''))
if ASA_ADDRESS not in _no_proxy:
    _no_proxy = (_no_proxy + ',' + ASA_ADDRESS).strip(',')
    os.environ['no_proxy'] = os.environ['NO_PROXY'] = _no_proxy
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
USERNAME = "admin"
PASSWORD = "Cisco@2026"
SYSLOG_SERVER_IP = "10.1.1.101"
IFNAME = "MGMT"
_SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION = 0x00000004
class _ASALegacySslAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.options |= _SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION
        pool_kwargs["ssl_context"] = ctx
        return super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)
def get_token():
    session = requests.Session()
    session.mount("https://", _ASALegacySslAdapter())
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    r = session.post(
        f"https://{ASA_ADDRESS}/api/tokenservices",
        auth=auth,
        headers={"Accept": "application/json"},
        verify=False,
    )
    r.raise_for_status()
    return r.headers["X-Auth-Token"]
def config_syslog(ifname, syslog_server_ip, token):
    url = f"https://{ASA_ADDRESS}/api/logging/syslogserver"
    data = {
        "ip": {
            "kind": "IPv4Address",
            "value": f"{syslog_server_ip}",
        },
        "interface": {
            "kind": "objectRef#Interface",
            "name": f"{ifname}",
        },
        "port": 514,
        "emblemEnabled": False,
        "secureEnabled": False,
        "protocol": "UDP",
    }
    session = requests.Session()
    session.mount("https://", _ASALegacySslAdapter())
    headers = {"Accept": "application/json", "X-Auth-Token": token}
    response = session.post(url, json=data, headers=headers, verify=False)
    print(f"状态码: {response.status_code}")
    try:
        print(response.json())
    except ValueError:
        print(response.text)
    return response
if __name__ == "__main__":
    token = get_token()
    print(f"获取 Token 成功")
    config_syslog(IFNAME, SYSLOG_SERVER_IP, token)
