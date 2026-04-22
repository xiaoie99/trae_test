#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚本使用 IMAP + mail-parser 实现邮件接收和附件下载
# 功能：连接IMAP服务器，解析邮件内容，下载附件，可选择删除服务器邮件
# IMAP 比 POP3 功能更强大，支持文件夹管理、搜索、标记等
#
# 依赖安装说明：
#   注意：pip 包名是 mail-parser（带连字符），而导入时用 mailparser（无连字符）
#   直接 pip install mailparser 会报 "No matching distribution found" 错误
#
#   在虚拟环境下安装：
#     source /Protocol2026/.venv/bin/activate
#     pip install mail-parser
#
#   验证安装：
#     python -c "import mailparser; print(mailparser.__version__)"

import os
import imaplib
import email
from pathlib import Path
from mailparser import parse_from_bytes  # 第三方库，专门用于解析邮件内容
from email.header import decode_header   # 用于解码邮件头部的编码（如base64、quoted-printable）

# 获取当前脚本所在目录，设置附件下载目录
current_file = Path(__file__)
current_dir = current_file.parent
attachment_dir = f"{current_dir}{os.sep}download_attachments{os.sep}"


def _ensure_attachment_dir_exists() -> None:
    """确保附件下载目录存在，如果不存在则创建"""
    Path(attachment_dir).mkdir(parents=True, exist_ok=True)


def qyt_rec_mail_imap(mailserver, mailuser, mailpasswd, mailbox='INBOX', if_write_dict=False, save_file=False, delete_email=False):
    """
    使用 IMAP + mail-parser 接收邮件并解析附件
    
    参数:
    - mailserver: IMAP服务器地址（如 imap.qq.com）
    - mailuser: 邮箱用户名
    - mailpasswd: 邮箱密码
    - mailbox: 邮箱文件夹（默认 INBOX）
    - if_write_dict: 是否将附件二进制内容写入字典（True=写入，False=只保存路径）
    - save_file: 是否保存附件到本地
    - delete_email: 是否删除服务器上的邮件
    
    返回:
    - 邮件字典列表，包含主题、发件人、收件人、正文、附件信息
    """
    print('Connecting to IMAP server...')
    # 使用 SSL 加密连接 IMAP 服务器（端口 993）
    server = imaplib.IMAP4_SSL(mailserver, 993)
    server.login(mailuser, mailpasswd)  # 登录邮箱
    mails_list = []
    
    try:
        # 选择邮箱文件夹（默认 INBOX）
        server.select(mailbox)
        
        # 搜索所有邮件（UNSEEN 表示未读邮件，ALL 表示所有邮件）
        status, messages = server.search(None, 'ALL')
        if status != 'OK':
            print('Failed to search emails')
            return []
            
        # 获取邮件ID列表
        email_ids = messages[0].split()
        print(f'Found {len(email_ids)} emails in {mailbox}')
        
        if save_file:
            _ensure_attachment_dir_exists()  # 确保附件下载目录存在

        # 处理每封邮件
        for email_id in email_ids:
            # 获取邮件内容
            status, msg_data = server.fetch(email_id, '(RFC822)')
            if status != 'OK':
                print(f'Failed to fetch email {email_id}')
                continue
                
            # 解析邮件
            raw_email = msg_data[0][1]
            
            # 使用 mail-parser 解析基本信息（主题、发件人、收件人、正文等）
            parsed = parse_from_bytes(raw_email)
            
            # 使用标准库 email 模块解析附件（更可靠的附件解析）
            email_msg = email.message_from_bytes(raw_email)

            mail_dict = {}

            # ========== 解析邮件头部信息 ==========
            # 使用 mail-parser 的头部信息，遍历所有头部字段
            headers_obj = getattr(parsed, 'headers', None)
            if isinstance(headers_obj, list):
                # 处理列表格式的头部信息
                for item in headers_obj:
                    name = None
                    value = None
                    if isinstance(item, dict) and 'name' in item and 'value' in item:
                        name = item['name']
                        value = item['value']
                    elif isinstance(item, (list, tuple)) and len(item) >= 2:
                        name = item[0]
                        value = item[1]
                    if not name:
                        continue
                    # 特别处理 Subject 字段，使用 mail-parser 的自动解码结果
                    if str(name).lower() == 'subject':
                        mail_dict['Subject'] = parsed.subject if getattr(parsed, 'subject', None) else value
                    else:
                        mail_dict[name] = value
            elif isinstance(headers_obj, dict):
                # 处理字典格式的头部信息
                for name, value in headers_obj.items():
                    if str(name).lower() == 'subject':
                        mail_dict['Subject'] = parsed.subject if getattr(parsed, 'subject', None) else value
                    else:
                        mail_dict[name] = value

            # 兜底设置 Subject（确保 Subject 字段存在）
            if 'Subject' not in mail_dict:
                mail_dict['Subject'] = parsed.subject if getattr(parsed, 'subject', None) else ''
            
            # ========== 修复 From 和 To 字段 ==========
            # 确保 From 字段有值
            if 'From' not in mail_dict or not mail_dict['From']:
                mail_dict['From'] = getattr(parsed, 'from_', [])
            
            # 修复 To 字段：检查是否为空或无效值（如 [('', '')]）
            current_to = mail_dict.get('To', [])
            is_empty_to = (not current_to or 
                          (isinstance(current_to, list) and 
                           all(isinstance(item, (list, tuple)) and 
                               (not item[0] and not item[1]) for item in current_to)))
            
            if is_empty_to:
                parsed_to = getattr(parsed, 'to', [])
                
                # 检查 parsed.to 是否也是空值
                parsed_is_empty = (not parsed_to or 
                                 (isinstance(parsed_to, list) and 
                                  all(isinstance(item, (list, tuple)) and 
                                      (not item[0] and not item[1]) for item in parsed_to)))
                
                if parsed_to and not parsed_is_empty:
                    mail_dict['To'] = parsed_to
                else:
                    # 从原始邮件头部直接提取 To 字段（绕过 mail-parser 解析问题）
                    to_header = email_msg.get('To', '')
                    
                    if to_header:
                        # 解析多个收件人（用分号分隔），统一格式为 [(邮箱地址, 邮箱地址)]
                        to_addresses = [addr.strip() for addr in to_header.split(';') if addr.strip()]
                        mail_dict['To'] = [(addr, addr) for addr in to_addresses]
                    else:
                        mail_dict['To'] = []

            # ========== 解析邮件正文 ==========
            # 初始化附件清单（包含所有附件和图片）
            mail_dict['Attachment'] = []

            # 解析邮件正文：优先使用纯文本，其次使用HTML
            body_text = ''
            try:
                if getattr(parsed, 'text_plain', None):
                    body_text = parsed.text_plain[0]  # 纯文本正文
                elif getattr(parsed, 'text_html', None):
                    body_text = parsed.text_html[0]  # HTML正文
            except Exception:
                body_text = ''
            if body_text:
                mail_dict['Body'] = body_text

            # ========== 解析附件（核心逻辑）==========
            # 使用标准库 email 模块解析附件（比 mail-parser 更可靠）
            for part in email_msg.walk():  # 遍历邮件的所有 MIME 部分
                content_disposition = part.get('Content-Disposition', '')  # 内容处置头
                content_type = part.get_content_type()  # 内容类型
                
                # 检查是否是附件（包括普通附件和内嵌图片）
                is_attachment = False
                filename = None
                
                # 1. 检查是否是明确的附件（Content-Disposition: attachment）
                if content_disposition and 'attachment' in content_disposition:
                    filename = part.get_filename()  # 获取附件文件名
                    is_attachment = True
                
                # 2. 检查是否是内嵌图片（Content-Type: image/*）
                elif content_type and content_type.startswith('image/'):
                    content_id = part.get('Content-ID', '')  # 内嵌图片的标识符
                    if content_id:
                        # 解码 Content-ID（可能被编码）
                        decoded_cid = decode_header(content_id)[0][0]
                        if isinstance(decoded_cid, bytes):
                            decoded_cid = decoded_cid.decode('utf-8', errors='ignore')
                        
                        # 清理 Content-ID 格式，生成图片文件名
                        cid_clean = decoded_cid.strip('<>')
                        ext = content_type.split('/')[-1] if '/' in content_type else 'bin'
                        filename = f"{cid_clean}.{ext}"
                        is_attachment = True
                
                # 处理附件
                if is_attachment and filename:
                    # 解码文件名（可能被 base64 或 quoted-printable 编码）
                    decoded_filename = decode_header(filename)[0][0]
                    if isinstance(decoded_filename, bytes):
                        decoded_filename = decoded_filename.decode('utf-8', errors='ignore')
                    
                    # 获取附件内容并自动解码
                    payload = part.get_payload(decode=True)
                    if payload:
                        # 总是将附件信息添加到列表中
                        attach_list = mail_dict.get('Attachment')
                        if if_write_dict:
                            # 将附件二进制内容写入字典（占用内存）
                            attach_list.append((decoded_filename, payload))
                        else:
                            # 只保存附件路径（节省内存）
                            attach_list.append((decoded_filename, attachment_dir + decoded_filename))
                        
                        # 根据 save_file 参数决定是否保存附件到本地
                        if save_file:
                            with open(attachment_dir + decoded_filename, 'wb') as fp:
                                fp.write(payload)

            # 将处理完的邮件添加到结果列表
            mails_list.append(mail_dict)

            # ========== 删除邮件（可选）==========
            if delete_email:
                # IMAP 删除邮件：标记为删除，然后 expunge
                server.store(email_id, '+FLAGS', '\\Deleted')
                
    finally:
        if delete_email:
            # 提交删除操作（真正删除标记为 Deleted 的邮件）
            server.expunge()
        # 关闭连接
        server.close()
        server.logout()

    return mails_list


if __name__ == '__main__':
    # ========== 主程序测试 ==========
    # 从环境变量获取邮箱账号密码
    smtp_user = os.environ.get('SMTPUSER')
    smtp_password = os.environ.get('SMTPPASS')
    from pprint import pprint
    
    i = 1
    # 调用 IMAP 邮件接收函数
    for x in qyt_rec_mail_imap('imap.qq.com',         # QQ邮箱IMAP服务器
                               smtp_user,              # 邮箱用户名
                               smtp_password,          # 邮箱密码
                               mailbox='INBOX',        # 邮箱文件夹（INBOX=收件箱）
                               if_write_dict=False,    # 不将附件二进制内容写入字典（节省内存）
                               save_file=True,         # 保存附件到本地
                               delete_email=True):     # 处理完后删除服务器上的邮件
        print('='*50, '第', i, '封信', '='*50)
        pprint(x)  # 美化打印邮件内容
        i += 1
