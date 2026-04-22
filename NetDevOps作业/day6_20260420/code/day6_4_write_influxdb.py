#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import sys

from influxdb import InfluxDBClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.tools.day6_snmp_get_all import snmpv2_get_all

DEVICES = [
    {"ip": "10.10.1.200", "community": "qytangro", "port": 161},
    {"ip": "10.10.1.201", "community": "qytangro", "port": 161},
]

INFLUX_CONFIG = {
    "host": "127.0.0.1",
    "port": 8086,
    "username": "qytdbuser",
    "password": "Cisc0123",
    "database": "qytdb",
    "measurement": "interface_monitor",
}


def write_once():
    client = InfluxDBClient(
        host=INFLUX_CONFIG["host"],
        port=INFLUX_CONFIG["port"],
        username=INFLUX_CONFIG["username"],
        password=INFLUX_CONFIG["password"],
        database=INFLUX_CONFIG["database"],
    )
    now = datetime.datetime.now(datetime.UTC).isoformat("T")

    payload = []
    for device in DEVICES:
        result = snmpv2_get_all(device["ip"], device["community"], device.get("port", 161))
        for if_info in result.get("interface_list", []):
            payload.append({
                "measurement": INFLUX_CONFIG["measurement"],
                "time": now,
                "tags": {
                    "device_ip": result["device_ip"],
                    "interface_name": if_info["interface_name"],
                },
                "fields": {
                    "in_bytes": if_info["in_bytes"],
                    "out_bytes": if_info["out_bytes"],
                },
            })
            print(
                f"[+] {result['device_ip']} {if_info['interface_name']:<30} "
                f"IN={if_info['in_bytes']:>12}  OUT={if_info['out_bytes']:>12}"
            )

    if payload:
        client.write_points(payload)
    print(f"[*] 共写入 {len(payload)} 条记录")


if __name__ == "__main__":
    write_once()
