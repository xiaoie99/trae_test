#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.day6_1_create_db import InternfaceMonitor, engine
from code.tools.day6_snmp_get_all import snmpv2_get_all

Session = sessionmaker(bind=engine)

DEVICES = [
    {"ip": "10.10.1.200", "community": "qytangro", "port": 161},
    {"ip": "10.10.1.201", "community": "qytangro", "port": 161},
]


def write_once():
    session = Session()
    total = 0
    try:
        for device in DEVICES:
            result = snmpv2_get_all(device["ip"], device["community"], device.get("port", 161))
            for if_info in result.get("interface_list", []):
                row = InternfaceMonitor(
                    device_ip=result["device_ip"],
                    interface_name=if_info["interface_name"],
                    in_bytes=if_info["in_bytes"],
                    out_bytes=if_info["out_bytes"],
                )
                session.add(row)
                total += 1
                print(
                    f"[+] {result['device_ip']} {if_info['interface_name']:<30} "
                    f"IN={if_info['in_bytes']:>12}  OUT={if_info['out_bytes']:>12}"
                )
        session.commit()
        print(f"[*] 共写入 {total} 条记录")
    finally:
        session.close()


if __name__ == "__main__":
    write_once()
