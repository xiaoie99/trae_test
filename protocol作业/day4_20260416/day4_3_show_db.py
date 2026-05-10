#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务五: 读取数据库, 绘制 Bokeh 折线图
从 SQLite 读取监控数据，绘制 CPU 和内存利用率趋势图
"""
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# 添加项目路径，确保模块导入正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools.day4_bokeh_line import bokeh_line
def read_recent_data(hours=1):
    """
    读取最近指定小时内的监控数据
    :param hours: 小时数，默认读取最近1小时数据
    :return: 按设备IP分组的数据字典
    """
    # 连接到数据库
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(script_dir, 'sqlalchemy_syslog_sqlite3.db')
    if not os.path.exists(db_file):
        print(f"[!] 错误: 数据库文件 {db_file} 不存在")
        return {}
    engine = create_engine(f'sqlite:///{db_file}', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    # 计算时间范围
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    # 查询最近数据
    query = text("""
        SELECT device_ip, cpu_useage_percent, mem_use, mem_free, record_datetime
        FROM router_monitor
        WHERE record_datetime >= :start_time
        ORDER BY device_ip, record_datetime
    """)
    result = session.execute(query, {'start_time': start_time})
    rows = result.fetchall()
    # 按设备IP分组数据
    device_data = {}
    for row in rows:
        device_ip = row[0]
        if device_ip not in device_data:
            device_data[device_ip] = {
                'time_list': [],
                'cpu_list': [],
                'mem_use_list': [],
                'mem_free_list': [],
                'mem_util_list': []
            }
        # 计算内存利用率
        mem_use = row[2]
        mem_free = row[3]
        mem_total = mem_use + mem_free
        mem_util = (mem_use / mem_total * 100) if mem_total > 0 else 0
        # 转换时间字符串为datetime对象
        time_str = row[4]
        if isinstance(time_str, str):
            # 处理不同的时间格式
            try:
                # 尝试解析带微秒的格式
                time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                try:
                    # 尝试解析不带微秒的格式
                    time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # 如果都无法解析，使用当前时间
                    time_obj = datetime.now()
        else:
            time_obj = time_str
        device_data[device_ip]['time_list'].append(time_obj)
        device_data[device_ip]['cpu_list'].append(row[1])
        device_data[device_ip]['mem_use_list'].append(mem_use)
        device_data[device_ip]['mem_free_list'].append(mem_free)
        device_data[device_ip]['mem_util_list'].append(mem_util)
    session.close()
    return device_data
def generate_cpu_chart(device_data):
    """生成CPU利用率趋势图"""
    lines_data = []
    for device_ip, data in device_data.items():
        if data['cpu_list']:  # 确保有数据
            lines_data.append([
                data['time_list'],
                data['cpu_list'],
                f"{device_ip}"
            ])
    if lines_data:
        # 生成CPU利用率趋势图
        bokeh_line(
            lines_data=lines_data,
            title='CPU利用率趋势',
            y_label='利用率 (%)'
        )
        return True
    return False
def generate_memory_chart(device_data):
    """生成内存利用率趋势图"""
    lines_data = []
    for device_ip, data in device_data.items():
        if data['mem_util_list']:  # 确保有数据
            lines_data.append([
                data['time_list'],
                data['mem_util_list'],
                f"{device_ip}"
            ])
    if lines_data:
        # 生成内存利用率趋势图
        bokeh_line(
            lines_data=lines_data,
            title='内存利用率趋势',
            y_label='利用率 (%)'
        )
        return True
    return False
def main():
    """主函数"""
    print("任务五: 读取数据库, 绘制 Bokeh 折线图")
    print("=" * 60)
    # 读取最近1小时数据
    print("[*] 读取最近1小时监控数据...")
    device_data = read_recent_data(hours=1)
    if not device_data:
        print("[!] 错误: 未读取到数据或数据库不存在")
        return
    # 显示读取结果
    for device_ip, data in device_data.items():
        record_count = len(data['time_list'])
        print(f"[*] {device_ip}: 读取 {record_count} 条记录")
    # 生成CPU利用率趋势图
    print("\n[*] 生成CPU利用率趋势图...")
    cpu_success = generate_cpu_chart(device_data)
    # 生成内存利用率趋势图
    print("[*] 生成内存利用率趋势图...")
    mem_success = generate_memory_chart(device_data)
    print("\n" + "=" * 60)
    if cpu_success and mem_success:
        print("任务五完成! Bokeh折线图已成功生成。")
        print("\n图表位置:")
        print("- CPU利用率趋势图: outputs/CPU利用率趋势.html")
        print("- 内存利用率趋势图: outputs/内存利用率趋势.html")
    else:
        print("任务五部分完成! 请检查数据是否足够。")
    print("=" * 60)
if __name__ == "__main__":
    main()