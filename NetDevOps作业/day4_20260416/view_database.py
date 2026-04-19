#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库查看工具 - 查看 router_monitor 表数据
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def view_database():
    """查看数据库内容"""
    print("数据库查看工具")
    print("=" * 60)
    # 连接到数据库（使用绝对路径解决Crond运行路径问题）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(script_dir, 'sqlalchemy_syslog_sqlite3.db')
    if not os.path.exists(db_file):
        print(f"[!] 错误: 数据库文件 {db_file} 不存在")
        return
    engine = create_engine(f'sqlite:///{db_file}', echo=False)
    try:
        with engine.connect() as conn:
            # 查看表结构
            print("[*] 表结构:")
            result = conn.execute(text("PRAGMA table_info(router_monitor)"))
            for row in result:
                print(f"    {row[1]} ({row[2]}) - {'主键' if row[5] else ''}")
            # 查看记录总数
            result = conn.execute(text("SELECT COUNT(*) FROM router_monitor"))
            total_records = result.scalar()
            print(f"\n[*] 总记录数: {total_records}")
            # 按设备统计
            print("\n[*] 按设备统计:")
            result = conn.execute(text("SELECT device_ip, COUNT(*) FROM router_monitor GROUP BY device_ip"))
            for row in result:
                print(f"    {row[0]}: {row[1]} 条记录")
            # 查看最近10条记录
            print("\n[*] 最近10条记录:")
            result = conn.execute(text("""
                SELECT id, device_ip, cpu_useage_percent, mem_use, mem_free, record_datetime 
                FROM router_monitor 
                ORDER BY id DESC 
                LIMIT 10
            """))
            print("    ID  | 设备IP       | CPU% | 已用内存    | 空闲内存    | 记录时间")
            print("    " + "-" * 70)
            for row in result:
                print(f"    {row[0]:<3} | {row[1]:<12} | {row[2]:<3}% | {row[3]:<10} | {row[4]:<10} | {row[5]}")
            # 查看CPU利用率统计
            print("\n[*] CPU利用率统计:")
            result = conn.execute(text("""
                SELECT device_ip, 
                       MIN(cpu_useage_percent) as 最小值,
                       MAX(cpu_useage_percent) as 最大值,
                       AVG(cpu_useage_percent) as 平均值
                FROM router_monitor 
                GROUP BY device_ip
            """))
            for row in result:
                print(f"    {row[0]}: 最小{row[1]}%, 最大{row[2]}%, 平均{row[3]:.1f}%")
    except Exception as e:
        print(f"[!] 数据库查询错误: {e}")
if __name__ == "__main__":
    view_database()
    print("\n" + "=" * 60)
    print("提示: 使用 sqlite3 命令行工具进行更详细的查询")
    print("命令: sqlite3 sqlalchemy_syslog_sqlite3.db")