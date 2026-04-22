#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

# ~~~~~~~~~~~~~~~~注意版本~~~~~~~~~~~~~
# pyasn1==0.6.1    # ~~~更新时间2025/2/23
# pysnmp==7.1.16   # ~~~更新时间2025/2/23

import asyncio
import pprint
import sys

from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv


DEFAULT_TRAP_PORT = 162
DEFAULT_LISTEN_ADDRESS = "0.0.0.0"


def cb_fun(snmp_engine, state_reference, context_engine_id, context_name, var_binds, cb_ctx):
    """SNMPv3 Trap 接收回调函数"""
    print("===== 收到SNMPv3陷阱 =====")

    result = {}

    try:
        if hasattr(context_engine_id, "asOctets"):
            engine_id_hex = "0x" + context_engine_id.asOctets().hex()
        else:
            engine_id_hex = "0x" + context_engine_id.prettyPrint().replace(":", "")
        result["engine_id"] = engine_id_hex
    except Exception:
        result["engine_id"] = str(context_engine_id.prettyPrint())

    result["context_name"] = str(context_name.prettyPrint())

    trap_data = {}
    for name, val in var_binds:
        trap_data[str(name.prettyPrint())] = str(val.prettyPrint())

    result["trap_data"] = trap_data

    pp = pprint.PrettyPrinter(indent=2, width=100, compact=False, sort_dicts=False)
    pp.pprint(result)
    print("===============================\n")

    return result


async def run_trap_receiver(listen_address,
                            trap_port,
                            username,
                            auth_key,
                            priv_key,
                            auth_protocol=usmHMACSHAAuthProtocol,
                            priv_protocol=usmAesCfb128Protocol):
    """运行 SNMPv3 Trap 接收器"""
    snmp_engine = engine.SnmpEngine()

    try:
        transport = udp.UdpTransport()
        config.add_transport(
            snmp_engine,
            udp.DOMAIN_NAME,
            transport.open_server_mode((listen_address, trap_port))
        )

        # 注册 SNMPv3 用户，用于验证和解密 Trap
        config.add_v3_user(
            snmp_engine,
            username,
            authProtocol=auth_protocol,
            authKey=auth_key,
            privProtocol=priv_protocol,
            privKey=priv_key
        )

        ntfrcv.NotificationReceiver(snmp_engine, cb_fun)

        print(f"SNMPv3陷阱接收器已启动 - 监听地址: {listen_address}:{trap_port}")
        print(f"用户名: {username}")
        print("按Ctrl+C退出...")

        while True:
            snmp_engine.transport_dispatcher.run_dispatcher(timeout=0.1)
            await asyncio.sleep(0.01)

    except PermissionError:
        print(f"错误: 没有足够权限绑定端口 {trap_port}")
        print("提示: 端口号小于1024需要管理员/root权限")
    except OSError as e:
        if e.errno == 98:
            print(f"错误: 端口 {trap_port} 已被占用")
        else:
            print(f"操作系统错误: {e}")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        print("\nSNMPv3陷阱接收器已停止")


def main():
    """主函数"""
    listen_address = DEFAULT_LISTEN_ADDRESS
    trap_port = DEFAULT_TRAP_PORT

    username = "qytanguser"
    auth_key = "Cisc0123"
    priv_key = "Cisc0123"

    print(f"正在启动SNMPv3陷阱接收器，监听地址: {listen_address}:{trap_port}")

    asyncio.run(
        run_trap_receiver(
            listen_address,
            trap_port,
            username,
            auth_key,
            priv_key,
            auth_protocol=usmHMACSHAAuthProtocol,
            priv_protocol=usmAesCfb128Protocol
        )
    )


if __name__ == "__main__":
    sys.exit(main())
