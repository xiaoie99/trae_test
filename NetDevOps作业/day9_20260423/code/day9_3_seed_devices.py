#!/usr/bin/env python3
# -*- coding=utf-8 -*-
"""Day 9 - 初始化测试设备清单"""
import os
import sys
import uuid
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)
from day9_1_model import Device, Session  # noqa: E402
TEST_DEVICES = [
    {
        'device_name': 'R1',
        'ip': '10.10.1.200',
        'username': 'admin',
        'password': 'qwert@12345',
        'enable_password': 'qwert@12345',
        'transport': 'ssh',
    },
    {
        'device_name': 'R2',
        'ip': '10.10.1.201',
        'username': 'admin',
        'password': 'qwert@12345',
        'enable_password': 'qwert@12345',
        'transport': 'ssh',
    },
]
def seed_devices():
    """把 Day 9 验证所需的测试设备写入数据库。"""
    session = Session()
    try:
        for device_info in TEST_DEVICES:
            device_obj = session.query(Device).filter_by(ip=device_info['ip']).first()
            if device_obj is None:
                device_obj = Device(
                    id=uuid.uuid4().hex,
                    device_name=device_info['device_name'],
                    ip=device_info['ip'],
                    username=device_info['username'],
                    password=device_info['password'],
                    enable_password=device_info['enable_password'],
                    transport=device_info['transport'],
                )
                session.add(device_obj)
                print(f"[+] 新增设备: {device_info['device_name']} {device_info['ip']}")
            else:
                device_obj.device_name = device_info['device_name']
                device_obj.username = device_info['username']
                device_obj.password = device_info['password']
                device_obj.enable_password = device_info['enable_password']
                device_obj.transport = device_info['transport']
                print(f"[*] 更新设备: {device_info['device_name']} {device_info['ip']}")
        session.commit()
        print(f'[+] 共处理 {len(TEST_DEVICES)} 台测试设备')
    finally:
        session.close()
if __name__ == '__main__':
    seed_devices()