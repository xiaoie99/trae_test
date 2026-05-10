#!/usr/bin/env python3
# -*- coding=utf-8 -*-
"""Day 9 - 初始化配置备份数据库"""
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)
from day9_1_model import Base, engine  # noqa: E402
def init_database():
    """创建 Day 9 使用的全部数据表。"""
    Base.metadata.create_all(engine, checkfirst=True)
    print('[+] Day 9 数据库表已经创建完成')
if __name__ == '__main__':
    init_database()