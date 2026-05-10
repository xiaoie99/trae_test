#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 创建 Syslog SQLite 数据库表（ORM 定义）
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime
import os
tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))
# 数据库文件存放在脚本同级目录
db_file_name = f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}sqlalchemy_syslog_sqlite3.db'
engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')
Base = declarative_base()
class Syslog(Base):
    """Syslog 日志记录表"""
    __tablename__ = 'syslog'
    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)  # 发送日志的设备 IP
    facility = Column(Integer, nullable=False)  # 设备模块编号
    facility_name = Column(String(64), nullable=False)  # 设备模块名称
    severity_level = Column(Integer, nullable=False)  # 严重级别编号
    severity_level_name = Column(String(64), nullable=False)  # 严重级别名称
    logid = Column(Integer, nullable=False)  # 日志序号
    log_source = Column(String(64), nullable=False)  # 日志来源模块
    description = Column(String(128), nullable=False)  # 日志描述
    text = Column(String(1024), nullable=False)  # 日志正文
    time = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)  # 日志时间
    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} | Datetime: {self.time} | Severity Name: {self.severity_level_name})"
if __name__ == '__main__':
    # 删除旧数据库文件，重新创建
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    # checkfirst=True 表示表已存在则跳过
    Base.metadata.create_all(engine, checkfirst=True)
