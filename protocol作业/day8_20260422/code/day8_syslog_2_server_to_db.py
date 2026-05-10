#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# Syslog UDP 服务器：接收日志 → 正则分词 → ORM 入库
import socketserver
import re
from dateutil import parser
from sqlalchemy.orm import sessionmaker
from day8_syslog_1_create_db import Syslog, engine
Session = sessionmaker(bind=engine)
session = Session()
# facility（设备模块）与编号对应关系
facility_dict = {0: 'KERN',
                 1: 'USER',
                 2: 'MAIL',
                 3: 'DAEMON',
                 4: 'AUTH',
                 5: 'SYSLOG',
                 6: 'LPR',
                 7: 'NEWS',
                 8: 'UUCP',
                 9: 'CRON',
                 10: 'AUTHPRIV',
                 11: 'FTP',
                 16: 'LOCAL0',
                 17: 'LOCAL1',
                 18: 'LOCAL2',
                 19: 'LOCAL3',
                 20: 'LOCAL4',
                 21: 'LOCAL5',
                 22: 'LOCAL6',
                 23: 'LOCAL7'}
# severity_level（严重级别）与名称对应关系
severity_level_dict = {0: 'EMERG',
                       1: 'ALERT',
                       2: 'CRIT',
                       3: 'ERR',
                       4: 'WARNING',
                       5: 'NOTICE',
                       6: 'INFO',
                       7: 'DEBUG'}
class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """接收UDP Syslog数据，使用正则解析后写入SQLite数据库。"""
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        print(data)
        syslog_info_dict = {'device_ip': self.client_address[0]}
        try:
            # 完整格式: <PRI>TIMESTAMP: %FACILITY-SEVERITY-MNEMONIC: message
            syslog_info = re.match(r'^<(\d*)>(\d*): (?:\w+: )?[.*]?(.*): %(\w+)-(\d)-(\w+): (.*)', str(data)).groups()
            syslog_info_dict['facility'] = int(syslog_info[0]) >> 3  # PRI 高5位为 facility
            syslog_info_dict['facility_name'] = facility_dict[int(syslog_info[0]) >> 3]
            syslog_info_dict['logid'] = int(syslog_info[1])
            syslog_info_dict['time'] = parser.parse(syslog_info[2])
            syslog_info_dict['log_source'] = syslog_info[3]
            syslog_info_dict['severity_level'] = int(syslog_info[4])
            syslog_info_dict['severity_level_name'] = severity_level_dict[int(syslog_info[4])]
            syslog_info_dict['description'] = syslog_info[5]
            syslog_info_dict['text'] = syslog_info[6]
        except AttributeError:
            # 部分日志缺失 %FACILITY-SEVERITY，改从 PRI 低3位提取 severity
            syslog_info = re.match(r'^<(\d*)>(\d*): (?:\w+: )?[.*]?(.*): (\w+): (.*)', str(data)).groups()
            syslog_info_dict['facility'] = int(syslog_info[0]) >> 3
            syslog_info_dict['facility_name'] = facility_dict[int(syslog_info[0]) >> 3]
            syslog_info_dict['logid'] = int(syslog_info[1])
            syslog_info_dict['time'] = parser.parse(syslog_info[2])
            syslog_info_dict['log_source'] = syslog_info[3]
            syslog_info_dict['severity_level'] = int(syslog_info[0]) & 0b111  # PRI 低3位为 severity
            syslog_info_dict['severity_level_name'] = severity_level_dict[(int(syslog_info[0]) & 0b111)]
            syslog_info_dict['description'] = 'N/A'
            syslog_info_dict['text'] = syslog_info[4]
        print(syslog_info_dict)
        syslog_record = Syslog(**syslog_info_dict)  # 字典直接展开为 ORM 字段
        session.add(syslog_record)
        session.commit()
if __name__ == "__main__":
    try:
        HOST, PORT = "0.0.0.0", 514
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        print("Syslog 服务已启用, 写入日志到数据库!!!")
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
    finally:
        for i in session.query(Syslog).all():
            print(i)
