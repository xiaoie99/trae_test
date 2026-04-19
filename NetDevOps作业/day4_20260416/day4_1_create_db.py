#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务三: 创建 SQLite 数据库表 (记录路由器 CPU 和内存)
使用 SQLAlchemy 创建 router_monitor 表
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 创建基类
Base = declarative_base()


class RouterMonitor(Base):
    """路由器监控数据表"""
    __tablename__ = 'router_monitor'
    
    # 主键，自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 设备 IP 地址 (字符串)
    device_ip = Column(String(15), nullable=False)
    
    # CPU 利用率百分比 (整数)
    cpu_useage_percent = Column(Integer, nullable=False)
    
    # 已用内存字节数 (整数)
    mem_use = Column(Integer, nullable=False)
    
    # 空闲内存字节数 (整数)
    mem_free = Column(Integer, nullable=False)
    
    # 记录时间 (自动取当前时间)
    record_datetime = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<RouterMonitor(device_ip='{self.device_ip}', cpu={self.cpu_useage_percent}%, " \
               f"mem_use={self.mem_use}, mem_free={self.mem_free}, time={self.record_datetime})>"


def create_database():
    """创建数据库和表"""
    print("任务三: 创建 SQLite 数据库表 (记录路由器 CPU 和内存)")
    print("=" * 60)
    
    # 创建数据库引擎（使用相对路径在当前目录下生成）
    db_file = 'sqlalchemy_syslog_sqlite3.db'
    engine = create_engine(f'sqlite:///{db_file}', echo=False)
    
    print(f"[*] 创建数据库引擎: {db_file}")
    
    # 创建所有表
    Base.metadata.create_all(engine)
    
    print("[*] 创建表结构:")
    print("    - router_monitor (路由器监控表)")
    print("        id (主键, 自增)")
    print("        device_ip (设备 IP 地址)")
    print("        cpu_useage_percent (CPU 利用率百分比)")
    print("        mem_use (已用内存字节数)")
    print("        mem_free (空闲内存字节数)")
    print("        record_datetime (记录时间)")
    
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 插入一些示例数据
    print("\n[*] 插入示例数据...")
    
    # 示例数据1
    record1 = RouterMonitor(
        device_ip='10.10.1.200',
        cpu_useage_percent=45,
        mem_use=256000000,
        mem_free=512000000
    )
    session.add(record1)
    
    # 示例数据2
    record2 = RouterMonitor(
        device_ip='10.10.1.201',
        cpu_useage_percent=32,
        mem_use=198000000,
        mem_free=420000000
    )
    session.add(record2)
    
    # 示例数据3
    record3 = RouterMonitor(
        device_ip='10.10.1.200',
        cpu_useage_percent=67,
        mem_use=312000000,
        mem_free=389000000
    )
    session.add(record3)
    
    # 提交事务
    session.commit()
    
    # 查询并显示插入的数据
    print("[*] 查询插入的数据:")
    records = session.query(RouterMonitor).all()
    for record in records:
        print(f"    {record}")
    
    # 关闭会话
    session.close()
    
    print(f"\n[*] 数据库创建完成!")
    print(f"[*] 生成的数据库文件: {db_file}")
    
    return db_file


def verify_database_file():
    """验证数据库文件是否生成"""
    import os
    
    db_file = 'sqlalchemy_syslog_sqlite3.db'
    if os.path.exists(db_file):
        file_size = os.path.getsize(db_file)
        print(f"\n[*] 验证数据库文件:")
        print(f"    - 文件存在: {db_file}")
        print(f"    - 文件大小: {file_size} 字节")
        return True
    else:
        print(f"\n[!] 错误: 数据库文件 {db_file} 未生成")
        return False


if __name__ == "__main__":
    # 创建数据库
    db_file = create_database()
    
    # 验证数据库文件
    verify_database_file()
    
    print("\n" + "=" * 60)
    print("任务三完成!")
    print("期望输出验证:")
    print("$ python3 day4_1_create_db.py")
    print("$ ls *.db")
    print("sqlalchemy_syslog_sqlite3.db")