#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 创建 Syslog SQLite 数据库表（ORM 定义）
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime
import os
tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))
db_file_name = f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}sqlalchemy_syslog_sqlite3.db'
engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')
Base = declarative_base()
class Syslog(Base):
    __tablename__ = 'syslog'
    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    facility = Column(Integer, nullable=False)
    facility_name = Column(String(64), nullable=False)
    severity_level = Column(Integer, nullable=False)
    severity_level_name = Column(String(64), nullable=False)
    logid = Column(Integer, nullable=False)
    log_source = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)
    text = Column(String(1024), nullable=False)
    time = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)
    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} | Datetime: {self.time} | Severity Name: {self.severity_level_name})"
if __name__ == '__main__':
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    Base.metadata.create_all(engine, checkfirst=True)
