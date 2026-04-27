#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 查看 SQLite 中 Syslog 记录的统计信息
from sqlalchemy.orm import sessionmaker
from day8_syslog_1_create_db import Syslog, engine
from sqlalchemy import func
Session = sessionmaker(bind=engine)
session = Session()
total = session.query(Syslog).count()
print(f'数据库中共有 {total} 条 Syslog 记录\n')
# 按严重级别统计
print('=== 按严重级别统计 ===')
for level, count in session.query(Syslog.severity_level_name, func.count(Syslog.severity_level_name)).group_by(
        Syslog.severity_level_name).all():
    print(f'    {level}: {count} 条')
print()
# 按设备统计
print('=== 按设备统计 ===')
for ip, count in session.query(Syslog.device_ip, func.count(Syslog.device_ip)).group_by(
        Syslog.device_ip).all():
    print(f'    {ip}: {count} 条')
print()
# 打印所有记录
print('=== 所有记录详情 ===')
for row in session.query(Syslog).all():
    print(f'    {row}')
