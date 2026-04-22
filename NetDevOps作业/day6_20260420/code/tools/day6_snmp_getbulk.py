#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pysnmp.hlapi.v3arch.asyncio import *


async def snmpv2_getbulk(ip, community, oid, count=50, port=161):
    iterator = bulk_cmd(
        SnmpEngine(),
        CommunityData(community),
        await UdpTransportTarget.create((ip, port)),
        ContextData(),
        0,
        count,
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=True,
    )
    error_indication, error_status, error_index, var_binds = await iterator

    if error_indication:
        raise RuntimeError(str(error_indication))
    if error_status:
        msg = f"{error_status} at {error_index and var_binds[int(error_index) - 1][0] or '?'}"
        raise RuntimeError(msg)

    result = []
    for row in var_binds:
        get_oid = str(row[0])
        get_value = str(row[1])
        if oid not in get_oid:
            break
        result.append((get_oid, get_value))
    return result
