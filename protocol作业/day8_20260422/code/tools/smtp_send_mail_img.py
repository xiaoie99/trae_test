#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# SMTP 邮件发送工具：支持内嵌 PNG 图片（Content-ID 方式）
import smtplib, email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
def qyt_smtp_img(mailserver, username, password, from_mail, to_mail, subj, main_body, images=None):
    """使用SSL加密SMTP发送HTML邮件，支持通过Content-ID方式内嵌图片。"""
    tos = to_mail.split(';')  # 多个收件人用分号分隔
    date = email.utils.formatdate()
    msg = MIMEMultipart()
    msg["Subject"] = subj
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Date"] = date
    part = MIMEText(main_body, 'html', 'utf-8')  # HTML 正文
    msg.attach(part)
    if images:
        for img in images:
            fp = open(img, 'rb')
            images_mime_part = MIMEImage(fp.read())
            fp.close()
            # Content-ID 的名字在 HTML 中用 cid:xxx 引用
            images_mime_part.add_header('Content-ID', os.path.basename(img).split('.')[0])
            msg.attach(images_mime_part)
    server = smtplib.SMTP_SSL(mailserver, 465)  # SSL 加密连接
    server.login(username, password)
    failed = server.sendmail(from_mail, tos, msg.as_string())
    server.quit()
    if failed:
        print('Falied recipients:', failed)
    else:
        print('邮件已经成功发出！')
if __name__ == '__main__':
    pass
