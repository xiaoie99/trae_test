#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def snmpv2_get(ip, community, oid, port=161):
    error_indication, error_status, error_index, var_binds = await get_cmd(
        SnmpEngine(),
        CommunityData(community),
        await UdpTransportTarget.create((ip, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    if error_indication:
        raise RuntimeError(str(error_indication))
    if error_status:
        msg = f"{error_status} at {error_index and var_binds[int(error_index) - 1][0] or '?'}"
        raise RuntimeError(msg)

    var_bind = var_binds[0]
    value = var_bind[1]
    if isinstance(value, bytes):
        result_str = bytes.fromhex(value[2:].decode("utf-8")).decode("utf-8", errors="ignore")
    else:
        result_str = str(value)
    return var_bind[0].prettyPrint(), result_str


if __name__ == "__main__":
    print(asyncio.run(snmpv2_get("10.10.1.200", "qytangro", "1.3.6.1.2.1.1.5.0")))
