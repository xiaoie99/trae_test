#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 从 SQLite 读取 Syslog 统计 → Pygal 生成饼图 → Jinja2 渲染 → 发送 HTML 邮件
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from day8_syslog_1_create_db import Syslog, engine
from sqlalchemy import func
from tools.day8_pygal_pie import pygal_pie
from tools.smtp_send_mail_img import qyt_smtp_img
from jinja2 import Template
load_dotenv()
current_dir = os.path.dirname(os.path.realpath(__file__))
tem_path = os.path.join(current_dir, 'templates')
with open(os.path.join(tem_path, 'syslog_email.template'), encoding='utf-8') as f:
    syslog_email_template = Template(f.read())
Session = sessionmaker(bind=engine)
session = Session()
# 查询严重级别统计
severity_level_name_list = []
severity_level_count_list = []
for level, count in session.query(Syslog.severity_level_name, func.count(Syslog.severity_level_name)).group_by(
        Syslog.severity_level_name).all():
    severity_level_name_list.append(level)
    severity_level_count_list.append(count)
# 查询设备统计
device_ip_list = []
device_log_count_list = []
for ip, count in session.query(Syslog.device_ip, func.count(Syslog.device_ip)).group_by(
        Syslog.device_ip).all():
    device_ip_list.append(ip)
    device_log_count_list.append(count)
# 生成 Pygal 饼状图 PNG
severity_level_filename = 'severity_level'
device_ip_filename = 'device_ip'
outputs_dir = os.path.join(current_dir, 'outputs')
os.makedirs(outputs_dir, exist_ok=True)
save_file_severity_level_file = os.path.join(outputs_dir, f"{severity_level_filename}.png")
save_file_device_ip_file = os.path.join(outputs_dir, f"{device_ip_filename}.png")
pygal_pie(severity_level_name_list, severity_level_count_list, 'SYSLOG严重级别分布图', save_file_severity_level_file)
pygal_pie(device_ip_list, device_log_count_list, 'SYSLOG设备分布图', save_file_device_ip_file)
# 整理为模板可渲染的列表（含百分比）
severity_total = sum(severity_level_count_list)
severity_level_count_html_list = []
for name, count in zip(severity_level_name_list, severity_level_count_list):
    percent = round(count / severity_total * 100, 2)
    severity_level_count_html_list.append({'name': name, 'log_count': count, 'percent': percent})
deice_log_total = sum(device_log_count_list)
device_ip_count_html_list = []
for ip, count in zip(device_ip_list, device_log_count_list):
    percent = round(count / deice_log_total * 100, 2)
    device_ip_count_html_list.append({'ip': ip, 'log_count': count, 'percent': percent})
# 渲染邮件 HTML
main_body_html = syslog_email_template.render(severity_level_count_html_list=severity_level_count_html_list,
                                              severity_level_filename=severity_level_filename,
                                              device_ip_count_html_list=device_ip_count_html_list,
                                              device_ip_filename=device_ip_filename)
# 读取环境变量并发送邮件
smtp_user = os.environ.get('SMTPUSER')
smtp_password = os.environ.get('SMTPPASS')
smtp_server = os.environ.get('SMTPSERVER')
smtp_from = os.environ.get('SMTPFROM')
qyt_smtp_img(smtp_server,
             smtp_user,
             smtp_password,
             smtp_from,
             '2950162785@qq.com;xiaochenglong99@163.com',
             '乾颐堂NetDevOps Syslog分析',
             main_body_html,
             [save_file_severity_level_file,
              save_file_device_ip_file])
