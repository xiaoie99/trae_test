#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from code.tools.day6_snmp_getbulk import snmpv2_getbulk


def _safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def snmpv2_get_all(ip_address, community, port=161):
    if_name_list = [x[1] for x in asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.2", port=port))]
    if_in_bytes_list = [x[1] for x in asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.10", port=port))]
    if_out_bytes_list = [x[1] for x in asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.16", port=port))]

    interface_list = []
    for name, in_bytes, out_bytes in zip(if_name_list, if_in_bytes_list, if_out_bytes_list):
        in_v = _safe_int(in_bytes)
        out_v = _safe_int(out_bytes)
        # 仅保留有字节计数的接口，减少噪声
        if in_v > 0 or out_v > 0:
            interface_list.append({
                "interface_name": name,
                "in_bytes": in_v,
                "out_bytes": out_v,
            })

    return {
        "device_ip": ip_address,
        "interface_list": interface_list,
    }
