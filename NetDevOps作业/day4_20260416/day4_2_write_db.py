#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务四: SNMP 采集 CPU/内存, 写入数据库 + Linux Crond 调度
使用 SNMP 采集思科设备性能数据并写入 SQLite 数据库
"""
import asyncio
import sys
import os
from datetime import datetime
# 添加项目路径，确保模块导入正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 自动处理Python环境问题（兼容原始Crond配置）
def auto_fix_python_environment():
    """自动处理Python环境，确保依赖包可用"""
    try:
        # 尝试导入必要的包
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        return True  # 环境正常
    except ImportError:
        # 环境异常，尝试自动修复
        print("[*] 检测到Python环境问题，尝试自动修复...")
        # 检查是否在虚拟环境中
        venv_path = '/python_basic/.venv'
        if os.path.exists(venv_path):
            # 尝试重新执行脚本使用虚拟环境Python
            venv_python = os.path.join(venv_path, 'bin', 'python')
            script_path = os.path.abspath(__file__)
            if os.path.exists(venv_python):
                print(f"[*] 重新执行脚本使用虚拟环境: {venv_python}")
                os.execl(venv_python, venv_python, script_path)
            else:
                print("[!] 虚拟环境Python不存在，请手动配置环境")
                return False
        else:
            print("[!] 虚拟环境不存在，请安装依赖包或配置虚拟环境")
            return False
    return False
# 在导入其他模块之前先检查环境
if not auto_fix_python_environment():
    sys.exit(1)
# 现在安全导入依赖包
from tools.day4_get import snmpv2_get
from day4_1_create_db import RouterMonitor, create_engine
from sqlalchemy.orm import sessionmaker
# 设备列表（根据实际情况修改IP和community）
DEVICES = [
    {"ip": "10.10.1.200", "community": "qytangro"},
    {"ip": "10.10.1.201", "community": "qytangro"}
]
# 思科设备 OID 定义
OIDS = {
    "cpu": "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7",        # CPU 5秒平均利用率
    "mem_used": "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7",  # 已用内存 (字节)
    "mem_free": "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7"   # 空闲内存 (字节)
}
async def snmp_collect_device(device_ip, community):
    """采集单个设备的SNMP数据"""
    try:
        # 采集CPU利用率
        _, cpu_str = await snmpv2_get(device_ip, community, OIDS["cpu"])
        cpu_percent = int(cpu_str) if cpu_str.isdigit() else 0
        # 采集已用内存
        _, mem_used_str = await snmpv2_get(device_ip, community, OIDS["mem_used"])
        mem_used = int(mem_used_str) if mem_used_str.isdigit() else 0
        # 采集空闲内存
        _, mem_free_str = await snmpv2_get(device_ip, community, OIDS["mem_free"])
        mem_free = int(mem_free_str) if mem_free_str.isdigit() else 0
        return {
            "ip": device_ip,
            "cpu_percent": cpu_percent,
            "mem_used": mem_used,
            "mem_free": mem_free,
            "success": True
        }
    except Exception as e:
        print(f"[!] 设备 {device_ip} 采集失败: {e}")
        return {
            "ip": device_ip,
            "cpu_percent": 0,
            "mem_used": 0,
            "mem_free": 0,
            "success": False
        }
def write_to_database(device_data):
    """将采集的数据写入数据库"""
    try:
        # 连接到数据库（使用绝对路径解决Crond运行路径问题）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_file = os.path.join(script_dir, 'sqlalchemy_syslog_sqlite3.db')
        engine = create_engine(f'sqlite:///{db_file}', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        # 创建记录对象
        record = RouterMonitor(
            device_ip=device_data["ip"],
            cpu_useage_percent=device_data["cpu_percent"],
            mem_use=device_data["mem_used"],
            mem_free=device_data["mem_free"]
        )
        # 添加到会话并提交
        session.add(record)
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(f"[!] 数据库写入失败: {e}")
        return False
async def main():
    """主函数：采集所有设备数据并写入数据库"""
    print("任务四: SNMP 采集 CPU/内存, 写入数据库")
    print("=" * 60)
    # 采集所有设备数据
    print("[*] 开始采集设备数据...")
    collected_data = []
    for device in DEVICES:
        print(f"[*] 采集设备: {device['ip']}")
        device_data = await snmp_collect_device(device["ip"], device["community"])
        collected_data.append(device_data)
    # 写入数据库并显示结果
    print("\n[*] 写入数据库...")
    success_count = 0
    for data in collected_data:
        if data["success"]:
            if write_to_database(data):
                print(f"[+] {data['ip']}: CPU={data['cpu_percent']}%, "
                      f"MEM_Used={data['mem_used']}, MEM_Free={data['mem_free']}")
                success_count += 1
            else:
                print(f"[!] {data['ip']}: 数据库写入失败")
        else:
            print(f"[!] {data['ip']}: 采集失败，跳过写入")
    print(f"\n[*] 共写入 {success_count} 条记录")
    # 显示当前时间（用于Crond调试）
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] 采集完成时间: {current_time}")
    return success_count
if __name__ == "__main__":
    # 运行主函数
    result = asyncio.run(main())
    print("\n" + "=" * 60)
    if result > 0:
        print("任务四完成! 数据已成功写入数据库。")
    else:
        print("任务四失败! 请检查设备连接和SNMP配置。")
    print("=" * 60)