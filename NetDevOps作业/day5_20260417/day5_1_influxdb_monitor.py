#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务: SNMP采集多台路由器CPU/内存写入InfluxDB
"""
import asyncio
import datetime
import os
import sys

from influxdb import InfluxDBClient

# 添加项目路径，确保模块导入正确（适配 crond）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools.day5_get import snmpv2_get


# 至少两台路由器
DEVICES = [
    {"ip": "10.10.1.200", "community": "qytangro", "device_type": "IOS-XE"},
    {"ip": "10.10.1.201", "community": "qytangro", "device_type": "IOS-XE"},
]

# Cisco 常用OID
OIDS = {
    "cpu_usage": "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7",
    "mem_used": "1.3.6.1.4.1.9.9.48.1.1.1.5.1",
    "mem_free": "1.3.6.1.4.1.9.9.48.1.1.1.6.1",
}

# InfluxDB 连接信息（与 compose 保持一致）
INFLUX_CONFIG = {
    "host": "127.0.0.1",
    "port": 8086,
    "username": "qytdbuser",
    "password": "Cisc0123",
    "database": "qytdb",
    "measurement": "router_monitor",
}


async def collect_device(device):
    ip = device["ip"]
    community = device["community"]
    try:
        _, cpu_str = await snmpv2_get(ip, community, OIDS["cpu_usage"])
        _, mem_used_str = await snmpv2_get(ip, community, OIDS["mem_used"])
        _, mem_free_str = await snmpv2_get(ip, community, OIDS["mem_free"])

        cpu_usage = int(cpu_str)
        mem_used = int(mem_used_str)
        mem_free = int(mem_free_str)
        mem_total = mem_used + mem_free
        mem_usage = round((mem_used / mem_total) * 100, 2) if mem_total else 0

        return {
            "success": True,
            "device_ip": ip,
            "device_type": device.get("device_type", "unknown"),
            "cpu_usage": cpu_usage,
            "mem_used": mem_used,
            "mem_free": mem_free,
            "mem_usage": mem_usage,
        }
    except Exception as e:
        return {"success": False, "device_ip": ip, "error": str(e)}


def write_influx(data_list):
    client = InfluxDBClient(
        host=INFLUX_CONFIG["host"],
        port=INFLUX_CONFIG["port"],
        username=INFLUX_CONFIG["username"],
        password=INFLUX_CONFIG["password"],
        database=INFLUX_CONFIG["database"],
    )

    current_time = datetime.datetime.now(datetime.UTC).isoformat("T")
    payload = []
    for item in data_list:
        payload.append({
            "measurement": INFLUX_CONFIG["measurement"],
            "time": current_time,
            "tags": {
                "device_ip": item["device_ip"],
                "device_type": item["device_type"],
            },
            "fields": {
                "cpu_usage": item["cpu_usage"],
                "mem_usage": item["mem_usage"],
                "mem_used": item["mem_used"],
                "mem_free": item["mem_free"],
            },
        })

    if payload:
        client.write_points(payload)
    return len(payload)


async def main():
    print("Day5: SNMP采集CPU/内存并写入InfluxDB")
    print("=" * 60)

    results = await asyncio.gather(*[collect_device(device) for device in DEVICES])
    success_data = []
    for result in results:
        if result["success"]:
            print(
                f"[+] {result['device_ip']} CPU={result['cpu_usage']}% "
                f"MEM={result['mem_usage']}% USED={result['mem_used']} FREE={result['mem_free']}"
            )
            success_data.append(result)
        else:
            print(f"[!] {result['device_ip']} 采集失败: {result['error']}")

    count = write_influx(success_data)
    print(f"[*] 本次写入InfluxDB记录数: {count}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
