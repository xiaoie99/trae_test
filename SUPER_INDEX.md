# 乾颐堂 Python / NetDevOps：课件（protocol2026）与作业超级索引

本文档覆盖 **`/python_basic/protocol2026`** 全部课件代码，以及 **`/python_basic`** 下 **`NetDevOps作业`**、**`python基础作业`**、**`1. 正则表达式`** 与根目录 **`test.py` / `new.py`**。

---

## 给新对话的 AI：如何使用本索引

**文档定位**：用一份「地图」替代在新对话里**通读**整个 `protocol2026` 与全部作业源码，从而减少重复加载课件所消耗的 Token。

**推荐工作流**

1. **先读本节与下方「目录」**，再按需跳转到第 1～6 节；不要默认把 `protocol2026` 下每个 `.py` 都完整读入上下文。
2. **根据用户给出的作业或问题**，结合第 **1** 节（树）、第 **2** 节（按文件）、第 **5** 节（作业速查），确定**最小相关文件列表**。
3. **仅当**需要核对实现细节、运行行为、或与课件逐行一致时，再在工作区**读取对应 `.py` 的完整内容**。
4. 回答时建议**简短说明**：依据了本索引里哪些路径/小节，以及额外打开了哪些源文件，方便用户确认是否为「按需阅读」。

**能力边界**：索引提供用途说明、类/函数**签名**、import、docstring 摘要等，**不包含**函数体与分支级逻辑；凡涉及「怎么写才对」的实现问题，**以源文件为准**。

**用户可复制给助手的开场模板**（将作业说明贴在末尾即可）：

```text
请先阅读工作区中的 SUPER_INDEX.md（建议至少：本节、《目录》、第 1～2 节、第 5 节），把它当作乾颐堂课件与作业的全局地图，不要默认通读 protocol2026 下所有源码。

然后根据下面作业要求，用索引定位相关文件；仅在需要实现细节时再读取具体 .py 的完整内容。

作业要求：
（在此粘贴题目或老师要求）
```

---

## 元数据

| 项 | 值 |
| --- | --- |
| 扫描 `.py` 文件数 | 258 |
| 解析方法 | `ast.parse` 模块级类/函数/导入；函数与类方法附带 `docstring` 首行（若有） |
| 维护建议 | 课件更新后重新运行仓库内生成脚本或让工具重新扫描以同步本索引 |

---

## 目录

1. [给新对话的 AI：如何使用本索引](#给新对话的-ai如何使用本索引)
2. [项目文件结构](#1-项目文件结构)
3. [模块与功能说明（按文件）](#2-模块与功能说明按文件)
4. [关键代码模式与模板](#3-关键代码模式与模板)
5. [跨文件调用关系](#4-跨文件调用关系)
6. [作业速查清单](#5-作业速查清单)
7. [从代码推断的规范与偏好](#6-从代码推断的规范与偏好)

---

## 1. 项目文件结构

以下为 **树状目录**：仅展开含 `.py` 的文件夹；每个 `.py` 一行，**破折号后**为一句话用途（优先模块文档字符串首行，否则为路径启发式）。

### 1.1 `protocol2026/`（协议与网络自动化课件）

- **basic_homework_day16/**
  - `__init__.py` — 学员作业/任务脚本
  - `day16_0_ssh_netmiko.py` — 学员作业/任务脚本
  - `day16_1_create_db_table.py` — 学员作业/任务脚本
  - `day16_2_get_config_insert_db.py` — 学员作业/任务脚本
- **net_10_smtp/**
  - **challenge_roud2/**
    - `challenge_roud2.py` — SMTP 挑战题
    - `qyt_smtp_attachment.py` — SMTP 发邮件
  - **modules/**
    - `__init__.py` — 课件或练习用 Python 脚本
    - `mat_bing.py` — 课件或练习用 Python 脚本
    - `syslog_bing.py` — Syslog 发送/落盘/服务端入库
  - **resend_email/**
    - `__init__.py` — 课件或练习用 Python 脚本
    - `resend_email.py` — 课件或练习用 Python 脚本
  - **word_pdf/**
    - `__init__.py` — Word 报告生成
    - `create_word_for_syslog.py` — Syslog 发送/落盘/服务端入库
    - `create_word_full.py` — Word 报告生成
  - `dingding_notify.py` — 钉钉通知
  - `smtp_send_mail_attachment.py` — SMTP 发邮件
  - `smtp_send_mail_img.py` — SMTP 发邮件
- **net_11_pop3/**
  - `__init__.py` — POP3 收邮件
  - `imap_mailparser.py` — POP3 收邮件
  - `pop3_mailparser.py` — POP3 收邮件
- **net_12_ldap/**
  - `ldap_query.py` — LDAP 查询与账号管理
  - `vip_ldap3.py` — LDAP 查询与账号管理
  - `vip_ldap3_0_get_pinyin_name.py` — LDAP 查询与账号管理
  - `vip_ldap3_0_login_info.py` — LDAP 查询与账号管理
  - `vip_ldap3_1_get_user_info.py` — LDAP 查询与账号管理
  - `vip_ldap3_2_get_group_users.py` — LDAP 查询与账号管理
  - `vip_ldap3_3_add_user.py` — LDAP 查询与账号管理
  - `vip_ldap3_4_remove_user.py` — LDAP 查询与账号管理
  - `vip_ldap3_5_disable_enable.py` — LDAP 查询与账号管理
  - `vip_ldap3_6_set_account_expires.py` — LDAP 查询与账号管理
  - `vip_ldap3_7_change_group.py` — LDAP 查询与账号管理
  - `vip_ldap3_8_changepassword.py` — LDAP 查询与账号管理
- **net_13_traffic_analysis/**
  - **pyshark_traffic_analysis/**
    - `__init__.py` — PyShark 解析与显示
    - `pyshark_0_pcap_dir.py` — PyShark 解析与显示
    - `pyshark_1_display.py` — PyShark 解析与显示
    - `pyshark_2_capture.py` — PyShark 解析与显示
    - `pyshark_3_options.py` — PyShark 解析与显示
    - `pyshark_4_analysis.py` — PyShark 解析与显示
    - `pyshark_5_1_tcpstream_maxid.py` — PyShark 解析与显示
    - `pyshark_5_2_tcpstream_get_tcp_stream.py` — PyShark 解析与显示
    - `pyshark_6_uri.py` — PyShark 解析与显示
  - **python_netflow/**
    - **db_dir/**
      - `__init__.py` — NetFlow v9 解析与存储
    - **new_mongodb_version/**
      - `mongo_config.py` — NetFlow v9 解析与存储
      - `netflow_parser_v9.py` — NetFlow v9 解析与存储
      - `netflow_server.py` — NetFlow v9 解析与存储
      - `report_html.py` — NetFlow v9 解析与存储
      - `reporter_app.py` — NetFlow v9 解析与存储
    - **new_orm_version/**
      - `__init__.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `netflow_orm_1_create_table.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `netflow_orm_2_v9_process_module.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `netflow_orm_3_collector_main.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `netflow_orm_4_show.py` — SQLAlchemy ORM：建表/写库/读库/展示
    - `__init__.py` — NetFlow v9 解析与存储
  - **scapy_traffic_analysis/**
    - `scapy_0_pcap_dir.py` — Scapy 处理 pcap/协议字段/实验
    - `scapy_1_pcap_syn_dos.py` — Scapy 处理 pcap/协议字段/实验
    - `scapy_2_pcap_http_uri.py` — Scapy 处理 pcap/协议字段/实验
    - `scapy_4_pcap_parser_keyword.py` — Scapy 处理 pcap/协议字段/实验
    - `scapy_5_tcp_rest.py` — Scapy 处理 pcap/协议字段/实验
    - `scapy_6_telnet_monitor.py` — Telnet 或 asyncio+Netmiko
    - `scapy_7_telnet_rst.py` — Telnet 或 asyncio+Netmiko
    - `scapy_8_telnet_rst_class.py` — Telnet 或 asyncio+Netmiko
  - `__init__.py` — 课件或练习用 Python 脚本
- **net_1_arp/**
  - `__init__.py` — 课件或练习用 Python 脚本
  - `arp_request.py` — ARP 请求/扫描/欺骗相关
  - `arp_scan_thread.py` — ARP 请求/扫描/欺骗相关
  - `arp_spoof.py` — ARP 请求/扫描/欺骗相关
  - `time_decorator.py` — 运行时间装饰器示例
- **net_2_icmp/**
  - `ping.py` — ICMP ping 单主机/扫描/IPv6
  - `ping_one.py` — ICMP ping 单主机/扫描/IPv6
  - `ping_scan.py` — ICMP ping 单主机/扫描/IPv6
  - `pingv6.py` — ICMP ping 单主机/扫描/IPv6
- **net_3_udp/**
  - `udp_socket_client.py` — UDP 套接字或 struct 打包示例
  - `udp_socket_server.py` — UDP 套接字或 struct 打包示例
  - `udp_struct_client.py` — UDP 套接字或 struct 打包示例
  - `udp_struct_server.py` — UDP 套接字或 struct 打包示例
- **net_4_snmp/**
  - **airflow/**
    - **dags/**
      - `__init__.py` — Airflow DAG 调度网络任务
      - `basic_info.py` — Airflow DAG 调度网络任务
      - `config_diff_0_ai.py` — Airflow DAG 调度网络任务
      - `config_diff_0_netmiko_show.py` — Netmiko 基础/模板/配置/异步
      - `config_diff_1_create_table.py` — Airflow DAG 调度网络任务
      - `config_diff_2_dff_conf.py` — Airflow DAG 调度网络任务
      - `config_diff_3_get_md5_config.py` — Airflow DAG 调度网络任务
      - `config_diff_4_dag.py` — Airflow DAG 调度网络任务
      - `orm_1_create_table.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `orm_2_write_db.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `orm_2_write_db_dag.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `qyt_send_mail.py` — Airflow DAG 调度网络任务
      - `snmp_v3_1_get.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
      - `snmp_v3_2_getbulk.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
      - `snmp_v3_3_get_all.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `__init__.py` — Airflow DAG 调度网络任务
  - **practice_lab/**
    - **lab1/**
      - `__init__.py` — 课件或练习用 Python 脚本
      - `orm_1_create_table.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `orm_2_write_db.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `orm_3_read_db_show_1_pygal.py` — SQLAlchemy ORM：建表/写库/读库/展示
      - `orm_3_read_db_show_2_bokeh.py` — SQLAlchemy ORM：建表/写库/读库/展示
    - **lab2/**
      - `influxdb_monitor_router.py` — SNMP + InfluxDB 路由器监控示例
  - **python_script/**
    - `__init__.py` — 课件或练习用 Python 脚本
    - `snmp_v2_1_get.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v2_2_set.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v2_3_getbulk.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v2_4_get_all.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v2_5_trap_server.py` — 简单的SNMPv2陷阱服务器（基于pysnmp库）
    - `snmp_v3_1_get.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v3_2_set.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v3_3_getbulk.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v3_4_get_all.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
    - `snmp_v3_5_trap_server.py` — SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
  - `__init__.py` — 课件或练习用 Python 脚本
- **net_5_syslog/**
  - **syslog/**
    - `__init__.py` — Syslog 发送/落盘/服务端入库
    - `syslog_client.py` — Syslog 发送/落盘/服务端入库
    - `syslog_server_to_file.py` — Syslog 发送/落盘/服务端入库
  - **syslog_write_db/**
    - `__init__.py` — Syslog 发送/落盘/服务端入库
    - `orm_1_syslog_create_table.py` — SQLAlchemy ORM：建表/写库/读库/展示
    - `orm_2_syslog_server_to_db.py` — SQLAlchemy ORM：建表/写库/读库/展示
    - `orm_3_syslog_show.py` — SQLAlchemy ORM：建表/写库/读库/展示
  - `__init__.py` — Syslog 发送/落盘/服务端入库
  - `nexus_syslog_example.py` — Syslog 发送/落盘/服务端入库
- **net_6_tcp/**
  - **socket_server/**
    - `__init__.py` — TCP 套接字服务端/客户端
    - `socket_client_from_input.py` — TCP 套接字服务端/客户端
    - `socket_client_from_list.py` — TCP 套接字服务端/客户端
    - `socket_server.py` — TCP 套接字服务端/客户端
  - **socket_server_json/**
    - `__init__.py` — TCP 套接字服务端/客户端
    - `socket_client_json.py` — TCP 套接字服务端/客户端
    - `socket_server_json.py` — TCP 套接字服务端/客户端
  - **socket_server_pickle/**
    - `__init__.py` — TCP 套接字服务端/客户端
    - `socket_client_pickle.py` — TCP 套接字服务端/客户端
    - `socket_server_pickle.py` — TCP 套接字服务端/客户端
  - `__init__.py` — 课件或练习用 Python 脚本
- **net_7_telnet/**
  - `asyncio_netmiko.py` — Telnet 或 asyncio+Netmiko
  - `netmiko_telnet_ssh.py` — Telnet 或 asyncio+Netmiko
  - `simple_telnet_client.py` — Telnet 或 asyncio+Netmiko
- **net_8_ssh/**
  - **netmiko_plan/**
    - **config_bak_and_diff/**
      - `__init__.py` — Netmiko 基础/模板/配置/异步
      - `config_diff_1_create_table.py` — Netmiko 基础/模板/配置/异步
      - `config_diff_2_dff_conf.py` — Netmiko 基础/模板/配置/异步
      - `config_diff_3_get_md5_config.py` — Netmiko 基础/模板/配置/异步
      - `config_diff_4_compare_config.py` — Netmiko 基础/模板/配置/异步
    - **excel_tools/**
      - `__init__.py` — Netmiko 基础/模板/配置/异步
      - `excel_opts_1_create.py` — Netmiko 基础/模板/配置/异步
      - `excel_opts_2_insert.py` — Netmiko 基础/模板/配置/异步
    - **jinja2_dir/**
      - `jinja2_python.py` — Netmiko 基础/模板/配置/异步
    - **web_front/**
      - **models/**
        - `__init__.py` — Netmiko 基础/模板/配置/异步
      - **routes/**
        - `__init__.py` — Netmiko 基础/模板/配置/异步
        - `areas.py` — Netmiko 基础/模板/配置/异步
        - `auth.py` — Netmiko 基础/模板/配置/异步
        - `credentials.py` — Netmiko 基础/模板/配置/异步
        - `devicetypes.py` — Netmiko 基础/模板/配置/异步
        - `interfaces.py` — Netmiko 基础/模板/配置/异步
        - `main.py` — Netmiko 基础/模板/配置/异步
        - `networks.py` — Netmiko 基础/模板/配置/异步
        - `ospf.py` — Netmiko 基础/模板/配置/异步
        - `routers.py` — Netmiko 基础/模板/配置/异步
        - `users.py` — Netmiko 基础/模板/配置/异步
      - `__init__.py` — Netmiko 基础/模板/配置/异步
      - `app.py` — Netmiko 基础/模板/配置/异步
      - `forms.py` — Netmiko 基础/模板/配置/异步
      - `run.py` — Netmiko 基础/模板/配置/异步
      - `utils.py` — Netmiko 基础/模板/配置/异步
    - **yaml_dir/**
      - `yaml_control.py` — Netmiko 基础/模板/配置/异步
    - `__init__.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_0_basic.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_1_show_client.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_2_ntc_template_1_basic.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_2_ntc_template_2_async.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_3_config_1_basic.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_3_config_2_async.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_3_config_db_0_async_netmiko.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_3_config_db_0_create_db.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_3_config_db_1_insert_db.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_3_config_db_2_config.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_4_1_from_excel.py` — Netmiko 基础/模板/配置/异步
    - `netmiko_4_2_to_excel.py` — Netmiko 基础/模板/配置/异步
  - **paramiko_plan/**
    - `__init__.py` — Paramiko SSH 执行命令
    - `ssh_client_multi_cmd.py` — Paramiko SSH 执行命令
    - `ssh_client_one_cmd.py` — Paramiko SSH 执行命令
  - **pyats/**
    - **pyats_2_learn/**
      - `pyats_2_learn_1_load_top_file.py` — Cisco pyATS 学习/对比/配置
      - `pyats_2_learn_2_load_list.py` — Cisco pyATS 学习/对比/配置
    - **pyats_3_diff/**
      - `pyats_3_diff_2_python.py` — Cisco pyATS 学习/对比/配置
    - **pyats_4_config/**
      - `pyats_4_config.py` — Cisco pyATS 学习/对比/配置
    - **pyats_5_job/**
      - `bgp_job.py` — Cisco pyATS 学习/对比/配置
      - `bgp_test.py` — Cisco pyATS 学习/对比/配置
    - **pytest/**
      - `pytest_ospf.py` — pytest 封装网络检查
      - `pytest_ping.py` — ICMP ping 单主机/扫描/IPv6
    - `pyats_1_netmiko.py` — Cisco pyATS 学习/对比/配置
  - **sftp_plan/**
    - `__init__.py` — FTP 列目录/上传/下载/查找
    - `sftp_client.py` — FTP 列目录/上传/下载/查找
  - `__init__.py` — 课件或练习用 Python 脚本
- **net_9_ftp/**
  - **file_dir/**
    - `qytang2.py` — 课件或练习用 Python 脚本
  - `ftp_find.py` — FTP 列目录/上传/下载/查找
  - `ftp_get.py` — FTP 列目录/上传/下载/查找
  - `ftp_list.py` — FTP 列目录/上传/下载/查找
  - `ftp_put.py` — FTP 列目录/上传/下载/查找
- **tools/**
  - `__init__.py` — 课件或练习用 Python 脚本
  - `change_ip_to_bytes.py` — IP 转字节
  - `change_mac_to_bytes.py` — MAC 转字节
  - `checksum.py` — 校验和工具
  - `decorator_time.py` — 装饰器工具
  - `get_ifname.py` — 接口名工具
  - `get_ip_netifaces.py` — 网卡 IP 获取
  - `get_mac_netifaces.py` — 网卡 MAC 获取
  - `scapy_iface.py` — Scapy 处理 pcap/协议字段/实验
  - `sort_ip.py` — IP 排序工具
  - `win_ifname.py` — Windows 接口名

### 1.2 `NetDevOps作业/`

- **day1_20260413/**
  - `day1_20260413_task1.py` — 学员作业/任务脚本
- **day2_20260414/**
  - `udp_client_test.py` — UDP 套接字或 struct 打包示例
  - `udp_server_test.py` — UDP 套接字或 struct 打包示例
- **day3_20260415/**
  - **code/**
    - **tools/**
      - `day3_bokeh_bing.py` — 学员作业/任务脚本
      - `day3_ssh_single_cmd.py` — 学员作业/任务脚本
    - `2026_day3_bokeh_netflow.py` — NetFlow v9 解析与存储
- **day4_20260416/**
  - **tools/**
    - `day4_bokeh_bar.py` — 学员作业/任务脚本
    - `day4_bokeh_line.py` — 学员作业/任务脚本
    - `day4_get.py` — 学员作业/任务脚本
  - `day4_1_create_db.py` — 任务三: 创建 SQLite 数据库表 (记录路由器 CPU 和内存)
  - `day4_2_write_db.py` — 任务四: SNMP 采集 CPU/内存, 写入数据库 + Linux Crond 调度
  - `day4_3_show_db.py` — 任务五: 读取数据库, 绘制 Bokeh 折线图
  - `view_database.py` — 数据库查看工具 - 查看 router_monitor 表数据
- **day5_20260417/**
  - **tools/**
    - `day5_get.py` — 学员作业/任务脚本
  - `day5_1_influxdb_monitor.py` — 任务: SNMP采集多台路由器CPU/内存写入InfluxDB
- **day6_20260420/**
  - **code/**
    - **tools/**
      - `__init__.py` — 学员作业/任务脚本
      - `day6_bokeh_line.py` — 学员作业/任务脚本
      - `day6_snmp_get.py` — 学员作业/任务脚本
      - `day6_snmp_get_all.py` — 学员作业/任务脚本
      - `day6_snmp_getbulk.py` — 学员作业/任务脚本
    - `__init__.py` — 学员作业/任务脚本
    - `day6_1_create_db.py` — 学员作业/任务脚本
    - `day6_2_write_sqlite.py` — 学员作业/任务脚本
    - `day6_3_show_sqlite.py` — 学员作业/任务脚本
    - `day6_4_write_influxdb.py` — 学员作业/任务脚本

### 1.3 `python基础作业/`

- **20260321/**
  - `3.py` — 创建一个Python脚本，打印一台网络设备的基本信息
  - `4.py` — 创建一个随机产生IP地址的代码
  - `5.py` — 打印一张简单的IP地址规划表
- **20260323/**
  - `1.py` — 定义以下变量，使用 f-string 打印一条网络设备的Syslog告警信息:
  - `2.py` — 现在有一个接口名字符串:
  - `3.py` — 从设备采集回来的版本信息字符串经常有多余的空格，需要处理后再使用:
  - `4.py` — 定义以下变量，使用 format() 打印一份格式整齐的接口状态报告:
- **20260324/**
  - `1.py` — 课件或练习用 Python 脚本
  - `2.py` — 课件或练习用 Python 脚本
- **20260325/**
  - `1.py` — 课件或练习用 Python 脚本
- **20260326/**
  - `1.py` — 课件或练习用 Python 脚本
  - `2.py` — 课件或练习用 Python 脚本
- **20260327/**
  - `1.py` — 课件或练习用 Python 脚本
  - `2.py` — 课件或练习用 Python 脚本
- **20260330/**
  - `1.py` — 课件或练习用 Python 脚本
- **20260402/**
  - `save_int_info.py` — 课件或练习用 Python 脚本
- **day08_20260331/**
  - `1.py` — 学员作业/任务脚本
  - `day08_task02_ping_gateway.py` — ICMP ping 单主机/扫描/IPv6
  - `my_server.py` — 学员作业/任务脚本
- **day09_20260401/**
  - `day09_task01_ssh_gateway.py` — 学员作业/任务脚本
- **day10_20260403/**
  - `day10_task1_cfg_change.py` — 学员作业/任务脚本
- **day12_20260406/**
  - `day12_task1_multicmd.py` — 学员作业/任务脚本
- **day13_20260407/**
  - `day13_task1.py` — 网络设备接口配置管理脚本
- **day14_20260408/**
  - `day14_task01_backup.py` — 学员作业/任务脚本
  - `day14_task02_ssh_argparse.py` — 学员作业/任务脚本
- **day15_20260409/**
  - `day15_task01.py` — 学员作业/任务脚本
- **day16_20260410/**
  - `day16_task01.py` — 学员作业/任务脚本

### 1.4 根目录与其它

- `test.py` — 课件或练习用 Python 脚本
- `new.py` — 课件或练习用 Python 脚本
- **1. 正则表达式/**
  - `demo.py` — 课件或练习用 Python 脚本

---

## 2. 模块与功能说明（按文件）

对**每个** `.py` 文件给出：用途概述、**类**（基类、类文档首行、方法签名与文档首行）、**模块级函数**、**启发式常量**（全大写赋值）、**import 摘要**。无类/无模块级函数会显式写「无」。

### `1. 正则表达式/demo.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `NetDevOps作业/day1_20260413/day1_20260413_task1.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `from scapy.all import Ether,ARP,sendp`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `NetDevOps作业/day2_20260414/udp_client_test.py`

- **概述**: UDP 套接字或 struct 打包示例
- **依赖 (import)**:
  - `socket`
  - `struct`
  - `hashlib`
  - `pickle`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `udp_send_data(ip, port, data_list)`

### `NetDevOps作业/day2_20260414/udp_server_test.py`

- **概述**: UDP 套接字或 struct 打包示例
- **依赖 (import)**:
  - `socket`
  - `sys`
  - `struct`
  - `hashlib`
  - `pickle`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `NetDevOps作业/day3_20260415/code/2026_day3_bokeh_netflow.py`

- **概述**: NetFlow v9 解析与存储
- **依赖 (import)**:
  - `re`
  - `from tools.day3_ssh_single_cmd import ssh_run`
  - `from tools.day3_bokeh_bing import bokeh_bing`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_netflow_app(host, username, password)` — SSH登录路由器, 采集Netflow数据, 正则提取, 绘制Bokeh饼状图。

### `NetDevOps作业/day3_20260415/code/tools/day3_bokeh_bing.py`

- **概述**: 学员作业/任务脚本
- **启发式常量**: `OUTPUTS_DIR`
- **依赖 (import)**:
  - `from bokeh.plotting import figure,output_file,save`
  - `from bokeh.transform import cumsum`
  - `from bokeh.palettes import Category10`
  - `pandas as pd`
  - `from math import pi`
  - `os`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `bokeh_bing(name_list, count_list, bing_name, save_name)` — 使用 Bokeh 绘制饼状图, 生成交互式 HTML 文件。

### `NetDevOps作业/day3_20260415/code/tools/day3_ssh_single_cmd.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `re`
  - `paramiko`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ssh_run(host, username, password, command)`

### `NetDevOps作业/day4_20260416/day4_1_create_db.py`

- **概述**: 任务三: 创建 SQLite 数据库表 (记录路由器 CPU 和内存)
- **依赖 (import)**:
  - `from sqlalchemy import create_engine,Column,Integer,String,DateTime`
  - `from sqlalchemy.ext.declarative import declarative_base`
  - `from sqlalchemy.orm import sessionmaker`
  - `from datetime import datetime`
- **类**:
  - **`RouterMonitor`**（基类: Base） — 路由器监控数据表
    - `__repr__(self)`
- **模块级函数**:
  - `create_database()` — 创建数据库和表
  - `verify_database_file()` — 验证数据库文件是否生成

### `NetDevOps作业/day4_20260416/day4_2_write_db.py`

- **概述**: 任务四: SNMP 采集 CPU/内存, 写入数据库 + Linux Crond 调度
- **启发式常量**: `DEVICES`, `OIDS`
- **依赖 (import)**:
  - `asyncio`
  - `sys`
  - `os`
  - `from datetime import datetime`
  - `from tools.day4_get import snmpv2_get`
  - `from day4_1_create_db import RouterMonitor,create_engine`
  - `from sqlalchemy.orm import sessionmaker`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmp_collect_device (async)(device_ip, community)` — 采集单个设备的SNMP数据
  - `write_to_database(device_data)` — 将采集的数据写入数据库
  - `main (async)()` — 主函数：采集所有设备数据并写入数据库

### `NetDevOps作业/day4_20260416/day4_3_show_db.py`

- **概述**: 任务五: 读取数据库, 绘制 Bokeh 折线图
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from datetime import datetime,timedelta`
  - `from sqlalchemy import create_engine,text`
  - `from sqlalchemy.orm import sessionmaker`
  - `from tools.day4_bokeh_line import bokeh_line`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `read_recent_data(hours)` — 读取最近指定小时内的监控数据
  - `generate_cpu_chart(device_data)` — 生成CPU利用率趋势图
  - `generate_memory_chart(device_data)` — 生成内存利用率趋势图
  - `main()` — 主函数

### `NetDevOps作业/day4_20260416/tools/day4_bokeh_bar.py`

- **概述**: 学员作业/任务脚本
- **启发式常量**: `OUTPUTS_DIR`
- **依赖 (import)**:
  - `from bokeh.plotting import figure,output_file,save`
  - `from bokeh.models import HoverTool,DatetimeTickFormatter,ColumnDataSource`
  - `os`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `bokeh_bar(time_list, value_list, line_name, title, y_label, save_name)` — 使用 Bokeh 绘制时间序列柱状图 (单设备单指标随时间变化)。

### `NetDevOps作业/day4_20260416/tools/day4_bokeh_line.py`

- **概述**: 学员作业/任务脚本
- **启发式常量**: `LINE_COLORS`, `OUTPUTS_DIR`
- **依赖 (import)**:
  - `from bokeh.plotting import figure,output_file,save`
  - `from bokeh.models import HoverTool,DatetimeTickFormatter,ColumnDataSource`
  - `os`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `bokeh_line(lines_data, title, y_label, save_name)` — 使用 Bokeh 绘制多条折线的时间序列图。

### `NetDevOps作业/day4_20260416/tools/day4_get.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_get (async)(ip, community, oid, port)`

### `NetDevOps作业/day4_20260416/view_database.py`

- **概述**: 数据库查看工具 - 查看 router_monitor 表数据
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from sqlalchemy import create_engine,text`
  - `from sqlalchemy.orm import sessionmaker`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `view_database()` — 查看数据库内容

### `NetDevOps作业/day5_20260417/day5_1_influxdb_monitor.py`

- **概述**: 任务: SNMP采集多台路由器CPU/内存写入InfluxDB
- **启发式常量**: `DEVICES`, `INFLUX_CONFIG`, `OIDS`
- **依赖 (import)**:
  - `asyncio`
  - `datetime`
  - `os`
  - `sys`
  - `from influxdb import InfluxDBClient`
  - `from tools.day5_get import snmpv2_get`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `collect_device (async)(device)`
  - `write_influx(data_list)`
  - `main (async)()`

### `NetDevOps作业/day5_20260417/tools/day5_get.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_get (async)(ip, community, oid, port)`

### `NetDevOps作业/day6_20260420/code/__init__.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `NetDevOps作业/day6_20260420/code/day6_1_create_db.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import declarative_base`
  - `from sqlalchemy import Column,String,Integer,DateTime,BigInteger`
  - `datetime`
  - `os`
- **类**:
  - **`InternfaceMonitor`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `NetDevOps作业/day6_20260420/code/day6_2_write_sqlite.py`

- **概述**: 学员作业/任务脚本
- **启发式常量**: `DEVICES`
- **依赖 (import)**:
  - `os`
  - `sys`
  - `from sqlalchemy.orm import sessionmaker`
  - `from code.day6_1_create_db import InternfaceMonitor,engine`
  - `from code.tools.day6_snmp_get_all import snmpv2_get_all`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `write_once()`

### `NetDevOps作业/day6_20260420/code/day6_3_show_sqlite.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `os`
  - `sys`
  - `from datetime import datetime,timedelta`
  - `numpy as np`
  - `from sqlalchemy.orm import sessionmaker`
  - `from code.day6_1_create_db import InternfaceMonitor,engine`
  - `from code.tools.day6_bokeh_line import bokeh_line`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `show_speed_from_db(minutes)` — 从 SQLite 读取最近 N 分钟数据, 用 Numpy 向量化计算速率, Bokeh 出图。

### `NetDevOps作业/day6_20260420/code/day6_4_write_influxdb.py`

- **概述**: 学员作业/任务脚本
- **启发式常量**: `DEVICES`, `INFLUX_CONFIG`
- **依赖 (import)**:
  - `datetime`
  - `os`
  - `sys`
  - `from influxdb import InfluxDBClient`
  - `from code.tools.day6_snmp_get_all import snmpv2_get_all`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `write_once()`

### `NetDevOps作业/day6_20260420/code/tools/__init__.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `NetDevOps作业/day6_20260420/code/tools/day6_bokeh_line.py`

- **概述**: 学员作业/任务脚本
- **启发式常量**: `LINE_COLORS`, `OUTPUTS_DIR`
- **依赖 (import)**:
  - `os`
  - `from pathlib import Path`
  - `from bokeh.models import ColumnDataSource,DatetimeTickFormatter,HoverTool`
  - `from bokeh.plotting import figure,output_file,save`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `bokeh_line(lines_data, title, y_label, save_name)`

### `NetDevOps作业/day6_20260420/code/tools/day6_snmp_get.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_get (async)(ip, community, oid, port)`

### `NetDevOps作业/day6_20260420/code/tools/day6_snmp_get_all.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `asyncio`
  - `from code.tools.day6_snmp_getbulk import snmpv2_getbulk`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `_safe_int(value, default)`
  - `snmpv2_get_all(ip_address, community, port)`

### `NetDevOps作业/day6_20260420/code/tools/day6_snmp_getbulk.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_getbulk (async)(ip, community, oid, count, port)`

### `new.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/basic_homework_day16/__init__.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/basic_homework_day16/day16_0_ssh_netmiko.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `from netmiko import Netmiko`
  - `hashlib`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_show_cred(host, username, password, cmd, enable, ssh)`
  - `compute_hash(s, algorithm)`
  - `get_show_run(host, username, password)`

### `protocol2026/basic_homework_day16/day16_1_create_db_table.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.ext.declarative import declarative_base`
  - `from sqlalchemy import Column,String,Integer,DateTime`
  - `datetime`
  - `from sqlalchemy.orm import sessionmaker`
- **类**:
  - **`RouterConfig`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `protocol2026/basic_homework_day16/day16_2_get_config_insert_db.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `from day16_1_create_db_table import RouterConfig,session`
  - `from day16_0_ssh_netmiko import get_show_run`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_10_smtp/challenge_roud2/challenge_roud2.py`

- **概述**: SMTP 挑战题
- **依赖 (import)**:
  - `sys`
  - `re`
  - `from qyt_email import qyt_smtp_attachment`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_10_smtp/challenge_roud2/qyt_smtp_attachment.py`

- **概述**: SMTP 发邮件
- **依赖 (import)**:
  - `os`
  - `smtplib`
  - `email.utils`
  - `from email.mime.multipart import MIMEMultipart`
  - `from email.mime.text import MIMEText`
  - `from email.mime.application import MIMEApplication`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `qyt_smtp_attachment(mailserver, username, password, from_mail, to_mail, subj, main_body, files)`

### `protocol2026/net_10_smtp/dingding_notify.py`

- **概述**: 钉钉通知
- **依赖 (import)**:
  - `os`
  - `from dingtalkchatbot.chatbot import DingtalkChatbot`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `send_group_msg(webhook, title, text, is_at_all)`

### `protocol2026/net_10_smtp/modules/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_10_smtp/modules/mat_bing.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `from matplotlib import pyplot as plt`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `mat_bing(size_list, name_list, save_file_name)`

### `protocol2026/net_10_smtp/modules/syslog_bing.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **依赖 (import)**:
  - `from matplotlib import pyplot as plt`
  - `from sqlalchemy.orm import sessionmaker`
  - `from sqlalchemy import create_engine`
  - `sys`
  - `from pathlib import Path`
  - `from net_5_syslog.syslog_write_db.orm_1_syslog_create_table import Syslog,db_file_name`
  - `from sqlalchemy import func`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `syslog_bing(save_file_name)`

### `protocol2026/net_10_smtp/resend_email/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_10_smtp/resend_email/resend_email.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `base64`
  - `resend`
  - `os`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `resend_email(email_from, email_to_list, subject, body, attachment_file_path_list)`

### `protocol2026/net_10_smtp/smtp_send_mail_attachment.py`

- **概述**: SMTP 发邮件
- **依赖 (import)**:
  - `os`
  - `smtplib`
  - `email.utils`
  - `from email.mime.multipart import MIMEMultipart`
  - `from email.mime.text import MIMEText`
  - `from email.mime.application import MIMEApplication`
  - `platform`
  - `sys`
  - `from pathlib import Path`
  - `from tools.decorator_time import print_run_time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `qyt_smtp_attachment(mailserver, username, password, from_mail, to_mail, subj, main_body, files)`

### `protocol2026/net_10_smtp/smtp_send_mail_img.py`

- **概述**: SMTP 发邮件
- **依赖 (import)**:
  - `re`
  - `smtplib`
  - `email.utils`
  - `from email.mime.multipart import MIMEMultipart`
  - `from email.mime.text import MIMEText`
  - `from email.mime.application import MIMEApplication`
  - `from email.mime.image import MIMEImage`
  - `os`
  - `sys`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `qyt_smtp_attachment(mailserver, username, password, from_mail, to_mail, subj, main_body, images)`

### `protocol2026/net_10_smtp/word_pdf/__init__.py`

- **概述**: Word 报告生成
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_10_smtp/word_pdf/create_word_for_syslog.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **依赖 (import)**:
  - `from docx import Document`
  - `from docx.enum.text import WD_ALIGN_PARAGRAPH`
  - `from docx.shared import Pt`
  - `from docx.oxml.ns import qn`
  - `from docx.shared import Inches`
  - `from docx.shared import RGBColor`
  - `sys`
  - `from pathlib import Path`
  - `from net_10_smtp.modules.syslog_bing import syslog_bing`
  - `os`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `create_word_for_syslog(add_img, save_word_name)`

### `protocol2026/net_10_smtp/word_pdf/create_word_full.py`

- **概述**: Word 报告生成
- **依赖 (import)**:
  - `time`
  - `from docx import Document`
  - `from docx.enum.text import WD_ALIGN_PARAGRAPH`
  - `from docx.shared import Pt`
  - `from docx.oxml.ns import qn`
  - `from docx.shared import Inches`
  - `from docx.shared import RGBColor`
  - `sys`
  - `from pathlib import Path`
  - `from net_10_smtp.modules.mat_bing import mat_bing`
  - `os`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `create_word_full(student_data, img_counters, img_protocols, save_word_name)`

### `protocol2026/net_11_pop3/__init__.py`

- **概述**: POP3 收邮件
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_11_pop3/imap_mailparser.py`

- **概述**: POP3 收邮件
- **依赖 (import)**:
  - `os`
  - `imaplib`
  - `email`
  - `from pathlib import Path`
  - `from mailparser import parse_from_bytes`
  - `from email.header import decode_header`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `_ensure_attachment_dir_exists()` → `None` — 确保附件下载目录存在，如果不存在则创建
  - `qyt_rec_mail_imap(mailserver, mailuser, mailpasswd, mailbox, if_write_dict, save_file, delete_email)` — 使用 IMAP + mail-parser 接收邮件并解析附件

### `protocol2026/net_11_pop3/pop3_mailparser.py`

- **概述**: POP3 收邮件
- **依赖 (import)**:
  - `os`
  - `poplib`
  - `base64`
  - `from pathlib import Path`
  - `from mailparser import parse_from_bytes`
  - `from email import message_from_bytes`
  - `from email.header import decode_header`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `_ensure_attachment_dir_exists()` → `None` — 确保附件下载目录存在，如果不存在则创建
  - `qyt_rec_mail(mailserver, mailuser, mailpasswd, if_write_dict, save_file, delete_email)` — 使用 POP3 + mail-parser 接收邮件并解析附件

### `protocol2026/net_12_ldap/ldap_query.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Server,Connection,AUTO_BIND_NO_TLS`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `qytldap(username, password)`

### `protocol2026/net_12_ldap/vip_ldap3.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Server,Connection,AUTO_BIND_NO_TLS,ALL,MODIFY_REPLACE`
  - `from datetime import timezone,timedelta,datetime,date`
  - `from dateutil import parser`
  - `pinyin`
  - `from random import randint,choice`
  - `string`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `random_password()`
  - `get_user_group(username, password)`
  - `get_group_users(user_dn)`
  - `disable_user(user_dn)`
  - `enable_user(user_dn)`
  - `get_user_attributes(cn)`
  - `if_user_expire_and_active(cn)`
  - `add_ad_user(xingming, phone, qq, mail, start_time, type)`
  - `disable_expired_users_by_group(group)`
  - `remove_user_from_group(user_dn, group_dn)`
  - `add_user_to_group(user_dn, group_dn)`
  - `change_user_password(user_dn, newpass)`
  - `overtime_user_accountexpires(user_dn, days)`
  - `set_user_accountexpires(user_dn, datetimeobj)`
  - `get_user_accountexpires(user_cn)`
  - `delete_user(cn)`
  - `get_username_dn(samaccountname)`
  - `delete_ccnp_user_by_username(samaccountname)`

### `protocol2026/net_12_ldap/vip_ldap3_0_get_pinyin_name.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `pinyin`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_pinyin_name(name)`

### `protocol2026/net_12_ldap/vip_ldap3_0_login_info.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Server,ALL`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_12_ldap/vip_ldap3_1_get_user_info.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_user_info(username)`
  - `get_user_self_info(username, password)`

### `protocol2026/net_12_ldap/vip_ldap3_2_get_group_users.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
  - `from vip_ldap3_1_get_user_info import get_user_info`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_group_users(group_name)`

### `protocol2026/net_12_ldap/vip_ldap3_3_add_user.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection,MODIFY_REPLACE`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
  - `from vip_ldap3_1_get_user_info import get_user_info`
  - `from vip_ldap3_0_get_pinyin_name import get_pinyin_name`
  - `from random import randint,choice`
  - `string`
  - `from datetime import timedelta,datetime`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `random_password()`
  - `add_ad_user(xingming, phone, qq, mail, group, random_pass)`

### `protocol2026/net_12_ldap/vip_ldap3_4_remove_user.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
  - `from vip_ldap3_1_get_user_info import get_user_info`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `delete_user(username)`

### `protocol2026/net_12_ldap/vip_ldap3_5_disable_enable.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection,MODIFY_REPLACE`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
  - `from vip_ldap3_1_get_user_info import get_user_info`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `disable_user(username)`
  - `enable_user(username)`

### `protocol2026/net_12_ldap/vip_ldap3_6_set_account_expires.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection,MODIFY_REPLACE`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
  - `from vip_ldap3_1_get_user_info import get_user_info`
  - `from datetime import datetime,timedelta`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `set_accountexpires(username, days)`
  - `set_user_accountexpires(username, datetimeobj)`

### `protocol2026/net_12_ldap/vip_ldap3_7_change_group.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
  - `from vip_ldap3_1_get_user_info import get_user_info`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `remove_user_from_group(username, groupname)`
  - `add_user_to_group(username, groupname)`

### `protocol2026/net_12_ldap/vip_ldap3_8_changepassword.py`

- **概述**: LDAP 查询与账号管理
- **依赖 (import)**:
  - `from ldap3 import Connection`
  - `sys`
  - `from pathlib import Path`
  - `from vip_ldap3_0_login_info import server,ad_admin_username,ad_admin_password`
  - `from vip_ldap3_1_get_user_info import get_user_info`
  - `from vip_ldap3_3_add_user import random_password`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `change_user_password(username, newpass)`

### `protocol2026/net_13_traffic_analysis/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/__init__.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_0_pcap_dir.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_1_display.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `pyshark`
  - `pprint`
  - `sys`
  - `from pathlib import Path`
  - `from pyshark_0_pcap_dir import pcap_data_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `print_highest_layer(pkt)`

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_2_capture.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `pyshark`
  - `pprint`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `print_highest_layer(pkt)`

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_3_options.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `pyshark`
  - `sys`
  - `from pathlib import Path`
  - `from pyshark_0_pcap_dir import pcap_data_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `print_highest_layer(pkt)`

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_4_analysis.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `pyshark`
  - `sys`
  - `from pathlib import Path`
  - `from pyshark_0_pcap_dir import pcap_data_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `print_highest_layer(pkt)`

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_5_1_tcpstream_maxid.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `pyshark`
  - `sys`
  - `from pathlib import Path`
  - `from pyshark_0_pcap_dir import pcap_data_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_max_id(pcap_file)`

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_5_2_tcpstream_get_tcp_stream.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `pyshark`
  - `sys`
  - `from pathlib import Path`
  - `from pyshark_0_pcap_dir import pcap_data_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_tcp_stream(pcap_file, sid)`

### `protocol2026/net_13_traffic_analysis/pyshark_traffic_analysis/pyshark_6_uri.py`

- **概述**: PyShark 解析与显示
- **依赖 (import)**:
  - `pyshark`
  - `re`
  - `os`
  - `from collections import defaultdict`
  - `sys`
  - `from pathlib import Path`
  - `from pyshark_0_pcap_dir import pcap_data_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `print_highest_layer(pkt)`

### `protocol2026/net_13_traffic_analysis/python_netflow/__init__.py`

- **概述**: NetFlow v9 解析与存储
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/python_netflow/db_dir/__init__.py`

- **概述**: NetFlow v9 解析与存储
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/python_netflow/new_mongodb_version/mongo_config.py`

- **概述**: NetFlow v9 解析与存储
- **启发式常量**: `MONGO_COLLECTION`, `MONGO_DB`, `MONGO_HOST`, `MONGO_PORT`
- **依赖 (import)**:
  - `os`
  - `from typing import Tuple`
  - `from pymongo import MongoClient`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_mongo()` → `Tuple[MongoClient, str, str]` — Return Mongo client, database name, and collection name.

### `protocol2026/net_13_traffic_analysis/python_netflow/new_mongodb_version/netflow_parser_v9.py`

- **概述**: NetFlow v9 解析与存储
- **启发式常量**: `FIELD_TYPES`, `_IPV4_FIELD_TYPES`, `_IPV6_FIELD_TYPES`, `_MAC_FIELD_TYPES`
- **依赖 (import)**:
  - `struct`
  - `ipaddress`
  - `from typing import Dict,Any,List`
- **类**:
  - **`TemplateField`**（基类: `object`）
    - `__init__(self, field_type, field_length)` → `None`
  - **`TemplateRecord`**（基类: `object`）
    - `__init__(self, template_id, fields)` → `None`
  - **`TemplateFlowSet`**（基类: `object`）
    - `__init__(self, data)` → `None`
  - **`DataFlowSet`**（基类: `object`）
    - `__init__(self, data, templates)` → `None`
  - **`ExportPacket`**（基类: `object`）
    - `__init__(self, data, templates)` → `None`
- **模块级函数**:
  - `ipv4_from_int(value)` → `str`
  - `mac_from_bytes(raw)` → `str`

### `protocol2026/net_13_traffic_analysis/python_netflow/new_mongodb_version/netflow_server.py`

- **概述**: NetFlow v9 解析与存储
- **启发式常量**: `BULK_SIZE`, `FLUSH_MS`, `HOST`, `MONGO_COLL`, `MONGO_DB`, `MONGO_HOST`, `MONGO_PORT`, `PORT`, `REUSEPORT`, `WRITE_CONCERN`
- **依赖 (import)**:
  - `os`
  - `socket`
  - `socketserver`
  - `threading`
  - `queue`
  - `signal`
  - `sys`
  - `from datetime import datetime,timezone`
  - `from typing import Dict,Optional`
  - `from pymongo import MongoClient,WriteConcern`
  - `from pymongo.collection import Collection`
  - `from netflow_parser_v9 import ExportPacket,TemplateRecord`
- **类**:
  - **`ThreadingUDPServer`**（基类: socketserver.ThreadingMixIn, socketserver.UDPServer）
    - `server_bind(self)` → `None`
  - **`NetflowUDPHandler`**（基类: socketserver.BaseRequestHandler）
    - `get_server(cls, host, port)`
    - `handle(self)`
- **模块级函数**:
  - `init_mongo()` → `None`
  - `close_mongo()` → `None`
  - `writer_thread_fn()` → `None` — Background writer that flushes by size or time.
  - `flush_batch(batch)` → `None`
  - `shutdown_handler(signum, frame)`

### `protocol2026/net_13_traffic_analysis/python_netflow/new_mongodb_version/report_html.py`

- **概述**: NetFlow v9 解析与存储
- **启发式常量**: `BUCKET_SEC`, `FONT_FAMILY`, `PALETTE`, `RANGE_MAP`
- **依赖 (import)**:
  - `os`
  - `json`
  - `from pathlib import Path`
  - `from typing import List,Tuple,Dict`
  - `from datetime import datetime,timedelta,timezone`
  - `from pymongo import MongoClient`
  - `plotly.graph_objects as go`
  - `plotly.io as pio`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_mongo_client()` → `MongoClient`
  - `get_collection(client)`
  - `make_time_filter(range_key)` → `Dict`
  - `bucket_params(range_key)` → `Tuple[str, int]`
  - `load_protocol_map()` → `Dict[int, str]`
  - `load_service_map()` → `Dict[str, str]` — Return mapping for application names.
  - `resolve_app_name(proto, port, proto_map, svc_map)` → `str`
  - `query_app_distribution(range_key, top_n)` → `List[Tuple[str, int]]`
  - `query_top_talkers(range_key, limit)` → `List[Tuple[str, int]]`
  - `query_timeseries_bps(range_key)` → `Tuple[List[str], List[float], str]` — Return (timestamps_iso, values_scaled, unit_str).
  - `apply_palette(fig, n)` → `None`
  - `style_fig(fig, title)` → `go.Figure`
  - `build_pie(title, labels, values)` → `go.Figure`
  - `build_app_distribution_figure(data)` → `go.Figure`
  - `build_top_talkers_figure(data)` → `go.Figure`
  - `build_timeseries_figure(times, values, unit_label)` → `go.Figure`
  - `generate_report_html(range_key)` → `str`

### `protocol2026/net_13_traffic_analysis/python_netflow/new_mongodb_version/reporter_app.py`

- **概述**: NetFlow v9 解析与存储
- **依赖 (import)**:
  - `os`
  - `from flask import Flask,Response,request`
  - `from report_html import generate_report_html`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `index()`

### `protocol2026/net_13_traffic_analysis/python_netflow/new_orm_version/__init__.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/python_netflow/new_orm_version/netflow_orm_1_create_table.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import declarative_base`
  - `from sqlalchemy import Column,String,Integer,DateTime`
  - `datetime`
  - `from pathlib import Path`
- **类**:
  - **`Netflow`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/python_netflow/new_orm_version/netflow_orm_2_v9_process_module.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `struct`
  - `from sqlalchemy.orm import sessionmaker`
  - `sys`
  - `from pathlib import Path`
  - `from netflow_orm_1_create_table import engine,Netflow`
- **类**:
  - **`IP`**（基类: `object`） — 读取数据,并且转换为字符串格式的IP地址
    - `__init__(self, data)`
  - **`DataFlowSet`**（基类: `object`） — 分析DataFlowSet内的字段和值
    - `__init__(self, data, templates)`
    - `__repr__(self)`
  - **`TemplateField`**（基类: `object`） — 仅仅用于记录模板中字段的类型和长度数据
    - `__init__(self, field_type, field_length)`
    - `__repr__(self)`
  - **`TemplateRecord`**（基类: `object`） — 仅仅用来记录模板内容,包括ID,数量和字段
    - `__init__(self, template_id, field_count, fields)`
    - `__repr__(self)`
  - **`TemplateFlowSet`**（基类: `object`） — 分析Template FlowSet,分析模板,便于后续分析Data FlowSet
    - `__init__(self, data)`
    - `__repr__(self)`
  - **`Header`**（基类: `object`） — 解析Netflow的头部
    - `__init__(self, data)`
  - **`ExportPacket`**（基类: `object`） — 这个类是整个解析的开头
    - `__init__(self, data, templates)`
    - `__repr__(self)`
- **模块级函数**:
  - `netflowdb(netflow_dict)`

### `protocol2026/net_13_traffic_analysis/python_netflow/new_orm_version/netflow_orm_3_collector_main.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `logging`
  - `sys`
  - `socketserver`
  - `from datetime import datetime`
  - `sys`
  - `from pathlib import Path`
  - `from netflow_orm_2_v9_process_module import ExportPacket`
- **类**:
  - **`SoftflowUDPHandler`**（基类: socketserver.BaseRequestHandler）
    - `get_server(cls, host, port)`
    - `handle(self)`
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/python_netflow/new_orm_version/netflow_orm_4_show.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `sqlite3`
  - `datetime`
  - `from matplotlib import pyplot as plt`
  - `from sqlalchemy.orm import sessionmaker`
  - `sys`
  - `from pathlib import Path`
  - `from netflow_orm_1_create_table import engine,Netflow`
  - `from sqlalchemy import func`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_0_pcap_dir.py`

- **概述**: Scapy 处理 pcap/协议字段/实验
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_1_pcap_syn_dos.py`

- **概述**: Scapy 处理 pcap/协议字段/实验
- **依赖 (import)**:
  - `warnings`
  - `from scapy.all import TCP,IP,rdpcap`
  - `from collections import defaultdict`
  - `sys`
  - `os`
  - `from pathlib import Path`
  - `from scapy_0_pcap_dir import pcap_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `find_pcap_syn_dos(pcap_filename)`

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_2_pcap_http_uri.py`

- **概述**: Scapy 处理 pcap/协议字段/实验
- **依赖 (import)**:
  - `warnings`
  - `from scapy.all import rdpcap,TCP,Raw`
  - `re`
  - `sys`
  - `from pathlib import Path`
  - `from scapy_0_pcap_dir import pcap_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `find_pcap_uri(pcap_filename, host_regex)`

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_4_pcap_parser_keyword.py`

- **概述**: Scapy 处理 pcap/协议字段/实验
- **依赖 (import)**:
  - `warnings`
  - `from scapy.all import *`
  - `re`
  - `sys`
  - `from pathlib import Path`
  - `from scapy_0_pcap_dir import pcap_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `pcap_parser(filename, keyword)`

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_5_tcp_rest.py`

- **概述**: Scapy 处理 pcap/协议字段/实验
- **依赖 (import)**:
  - `warnings`
  - `from scapy.all import TCP,IP,Ether,sendp,sniff`
  - `sys`
  - `from pathlib import Path`
  - `from tools.scapy_iface import scapy_iface`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `tcp_monitor_callback(pkt)`
  - `tcp_reset(src_ip, dst_ip, dst_port, ifname, src_port)`

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_6_telnet_monitor.py`

- **概述**: Telnet 或 asyncio+Netmiko
- **依赖 (import)**:
  - `warnings`
  - `re`
  - `from scapy.all import Raw,sniff,wrpcap`
  - `hexdump`
  - `sys`
  - `from pathlib import Path`
  - `from tools.scapy_iface import scapy_iface`
  - `from net_13_traffic_analysis.scapy_traffic_analysis.scapy_0_pcap_dir import pcap_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `qythexdump(src, length)`
  - `telnet_monitor_callback(pkt)`
  - `telnet_monitor(user_filter, ifname)`

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_7_telnet_rst.py`

- **概述**: Telnet 或 asyncio+Netmiko
- **依赖 (import)**:
  - `warnings`
  - `re`
  - `from scapy.all import TCP,IP,Ether,sendp,sniff,wrpcap,Raw`
  - `sys`
  - `from pathlib import Path`
  - `from tools.scapy_iface import scapy_iface`
  - `from net_13_traffic_analysis.scapy_traffic_analysis.scapy_0_pcap_dir import pcap_dir`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `reset_tcp(pkt)`
  - `telnet_monitor_callback(pkt)`
  - `telnet_rst(user_filter, ifname)`

### `protocol2026/net_13_traffic_analysis/scapy_traffic_analysis/scapy_8_telnet_rst_class.py`

- **概述**: Telnet 或 asyncio+Netmiko
- **依赖 (import)**:
  - `logging`
  - `warnings`
  - `re`
  - `sys`
  - `argparse`
  - `from pathlib import Path`
  - `from scapy.all import TCP,IP,Ether,sendp,sniff,wrpcap,Raw`
  - `from tools.scapy_iface import scapy_iface`
  - `from net_13_traffic_analysis.scapy_traffic_analysis.scapy_0_pcap_dir import pcap_dir`
- **类**:
  - **`TelnetMonitor`**（基类: `object`） — Telnet会话监控和RST攻击类
    - `__init__(self, interface, filter_str, timeout, debug)` — 初始化Telnet监控器
    - `reset_tcp(self, pkt)` — 发送TCP RST包重置连接
    - `packet_callback(self, pkt)` — 处理捕获的数据包
    - `start(self)` — 开始捕获和监控Telnet流量
- **模块级函数**: （无）

### `protocol2026/net_1_arp/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_1_arp/arp_request.py`

- **概述**: ARP 请求/扫描/欺骗相关
- **依赖 (import)**:
  - `from scapy.all import ARP,sr1`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `arp_request(ip_address)`

### `protocol2026/net_1_arp/arp_scan_thread.py`

- **概述**: ARP 请求/扫描/欺骗相关
- **依赖 (import)**:
  - `ipaddress`
  - `from multiprocessing.pool import ThreadPool`
  - `sys`
  - `from pathlib import Path`
  - `from net_1_arp.arp_request import arp_request`
  - `from net_1_arp.time_decorator import run_time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `scapy_arp_scan(network)` — ARP扫描

### `protocol2026/net_1_arp/arp_spoof.py`

- **概述**: ARP 请求/扫描/欺骗相关
- **依赖 (import)**:
  - `from scapy.all import ARP,Ether,sendp`
  - `time`
  - `signal`
  - `sys`
  - `from pathlib import Path`
  - `from tools.get_ip_netifaces import get_ip_address`
  - `from tools.get_mac_netifaces import get_mac_address`
  - `from tools.scapy_iface import scapy_iface`
  - `from net_1_arp.arp_request import arp_request`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `arp_spoof(ip_1, ip_2, ifname)`
  - `sigint_handler(signum, frame)`

### `protocol2026/net_1_arp/time_decorator.py`

- **概述**: 运行时间装饰器示例
- **依赖 (import)**:
  - `from functools import wraps`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `run_time()`

### `protocol2026/net_2_icmp/ping.py`

- **概述**: ICMP ping 单主机/扫描/IPv6
- **依赖 (import)**:
  - `from scapy.all import IP,ICMP,Raw,Padding,sr1`
  - `time`
  - `struct`
  - `random`
  - `sys`
  - `re`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ping_one(dst, id_no, seq_no, ttl_no)`
  - `qyt_ping(dst)`

### `protocol2026/net_2_icmp/ping_one.py`

- **概述**: ICMP ping 单主机/扫描/IPv6
- **依赖 (import)**:
  - `from scapy.all import ICMP,IP,sr1`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `scapy_ping_one(host)`

### `protocol2026/net_2_icmp/ping_scan.py`

- **概述**: ICMP ping 单主机/扫描/IPv6
- **依赖 (import)**:
  - `ipaddress`
  - `sys`
  - `os`
  - `from multiprocessing.pool import ThreadPool as Pool`
  - `from pathlib import Path`
  - `from net_2_icmp.ping_one import scapy_ping_one`
  - `from tools.sort_ip import sort_ip`
  - `from net_1_arp.time_decorator import run_time`
- **类**:
  - **`NullDevice`**（基类: `object`）
    - `write(self, s)`
    - `flush(self)`
- **模块级函数**:
  - `scapy_ping_scan(network)`

### `protocol2026/net_2_icmp/pingv6.py`

- **概述**: ICMP ping 单主机/扫描/IPv6
- **依赖 (import)**:
  - `from scapy.all import IPv6,ICMPv6EchoRequest,sr1`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `scapy_pingv6_one(host)`

### `protocol2026/net_3_udp/udp_socket_client.py`

- **概述**: UDP 套接字或 struct 打包示例
- **依赖 (import)**:
  - `socket`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_3_udp/udp_socket_server.py`

- **概述**: UDP 套接字或 struct 打包示例
- **依赖 (import)**:
  - `socket`
  - `sys`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_3_udp/udp_struct_client.py`

- **概述**: UDP 套接字或 struct 打包示例
- **依赖 (import)**:
  - `socket`
  - `struct`
  - `hashlib`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_3_udp/udp_struct_server.py`

- **概述**: UDP 套接字或 struct 打包示例
- **依赖 (import)**:
  - `socket`
  - `struct`
  - `sys`
  - `hashlib`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/__init__.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/dags/__init__.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/dags/basic_info.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/dags/config_diff_0_ai.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - `from openai import OpenAI`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ai_diff(diff_config)`

### `protocol2026/net_4_snmp/airflow/dags/config_diff_0_netmiko_show.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from netmiko import Netmiko`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_show_cred(host, username, password, cmd, device_type, use_textfsm, ssh_port)`

### `protocol2026/net_4_snmp/airflow/dags/config_diff_1_create_table.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import declarative_base`
  - `from sqlalchemy import Column,String,Integer,DateTime`
  - `datetime`
- **类**:
  - **`RouterConfig`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/dags/config_diff_2_dff_conf.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - `difflib`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `html_diff_snippet(txt1, txt2, context)`

### `protocol2026/net_4_snmp/airflow/dags/config_diff_3_get_md5_config.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - `re`
  - `hashlib`
  - `from datetime import datetime`
  - `os`
  - `from pathlib import Path`
  - `sys`
  - `from sqlalchemy.orm import sessionmaker`
  - `from config_diff_1_create_table import RouterConfig`
  - `from config_diff_2_dff_conf import html_diff_snippet`
  - `from qyt_send_mail import qyt_smtp_attachment_html`
  - `from jinja2 import Template`
  - `from sqlalchemy import create_engine`
  - `from config_diff_0_ai import ai_diff`
  - `from config_diff_0_netmiko_show import netmiko_show_cred`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_md5_config(host, username, password)`
  - `config_diff_and_notification()`

### `protocol2026/net_4_snmp/airflow/dags/config_diff_4_dag.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - `from datetime import datetime,timedelta`
  - `from airflow import DAG`
  - `from airflow.operators.python import PythonOperator`
  - `from config_diff_3_get_md5_config import config_diff_and_notification`
  - `from qyt_send_mail import qyt_smtp_attachment`
  - `pendulum`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/dags/orm_1_create_table.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **启发式常量**: `GMT_PLUS_8`
- **依赖 (import)**:
  - `from datetime import datetime,timedelta,timezone`
  - `from sqlalchemy import create_engine,orm`
  - `from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Float`
- **类**:
  - **`RouterMonitor`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/dags/orm_2_write_db.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `time`
  - `from snmp_v3_3_get_all import snmpv3_get_all`
  - `from sqlalchemy.orm import sessionmaker`
  - `from orm_1_create_table import RouterMonitor,engine`
  - `from datetime import timezone,timedelta,datetime`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_info_writedb(ip_address, username, auth_key, priv_key)`

### `protocol2026/net_4_snmp/airflow/dags/orm_2_write_db_dag.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `from datetime import datetime,timedelta`
  - `from airflow import DAG`
  - `from airflow.operators.python import PythonOperator`
  - `from orm_2_write_db import get_info_writedb,ip_address,username,auth_key,priv_key`
  - `from qyt_send_mail import qyt_smtp_attachment`
  - `pendulum`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/airflow/dags/qyt_send_mail.py`

- **概述**: Airflow DAG 调度网络任务
- **依赖 (import)**:
  - `smtplib`
  - `email.utils`
  - `from email.mime.multipart import MIMEMultipart`
  - `from email.mime.text import MIMEText`
  - `from basic_info import tos,email_username,email_password,email_from`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `qyt_smtp_attachment(context)`
  - `qyt_smtp_attachment_html(mailserver, username, password, from_mail, to_mail, subj, main_body, images)`

### `protocol2026/net_4_snmp/airflow/dags/snmp_v3_1_get.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv3_get (async)(ip, username, auth_key, priv_key, oid, auth_protocol, priv_protocol, port)`

### `protocol2026/net_4_snmp/airflow/dags/snmp_v3_2_getbulk.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv3_getbulk (async)(ip, username, auth_key, priv_key, oid, count, auth_protocol, priv_protocol, port)`

### `protocol2026/net_4_snmp/airflow/dags/snmp_v3_3_get_all.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from snmp_v3_1_get import snmpv3_get`
  - `from snmp_v3_2_getbulk import snmpv3_getbulk`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv3_get_all(ip_address, username, auth_key, priv_key)`

### `protocol2026/net_4_snmp/practice_lab/lab1/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/practice_lab/lab1/orm_1_create_table.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import declarative_base`
  - `from sqlalchemy import Column,String,Integer,DateTime`
  - `datetime`
  - `from pathlib import Path`
  - `os`
- **类**:
  - **`RouterMonitor`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/practice_lab/lab1/orm_2_write_db.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from pathlib import Path`
  - `from sqlalchemy.orm import sessionmaker`
  - `from sqlalchemy import create_engine`
  - `from python_script.snmp_v3_4_get_all import snmpv3_get_all`
  - `from orm_1_create_table import RouterMonitor,db_filename`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_info_writedb(ip_address, username, auth_key, priv_key)`

### `protocol2026/net_4_snmp/practice_lab/lab1/orm_3_read_db_show_1_pygal.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from pathlib import Path`
  - `from sqlalchemy.orm import sessionmaker`
  - `from orm_1_create_table import RouterMonitor,db_filename`
  - `pygal`
  - `from pygal.style import Style`
  - `from sqlalchemy import create_engine`
  - `from datetime import datetime,timedelta`
  - `cairosvg`
  - `os`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `cpu_show(filename)`
  - `mem_show(filename)`

### `protocol2026/net_4_snmp/practice_lab/lab1/orm_3_read_db_show_2_bokeh.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from pathlib import Path`
  - `from sqlalchemy.orm import sessionmaker`
  - `from orm_1_create_table import RouterMonitor,db_filename`
  - `from sqlalchemy import create_engine`
  - `from datetime import datetime,timedelta`
  - `from bokeh.plotting import figure,output_file,save`
  - `from bokeh.models import DatetimeTickFormatter,HoverTool`
  - `numpy as np`
  - `from scipy.interpolate import make_interp_spline`
  - `pytz`
  - `os`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `smooth_data(x, y, points)` — 使用样条插值平滑曲线
  - `cpu_show(filename)`
  - `mem_show(filename)`

### `protocol2026/net_4_snmp/practice_lab/lab2/influxdb_monitor_router.py`

- **概述**: SNMP + InfluxDB 路由器监控示例
- **依赖 (import)**:
  - `from pathlib import Path`
  - `sys`
  - `from python_script.snmp_v2_4_get_all import snmpv2_get_all`
  - `time`
  - `datetime`
  - `from influxdb import InfluxDBClient`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/python_script/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_4_snmp/python_script/snmp_v2_1_get.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_get (async)(ip, community, oid, port)`

### `protocol2026/net_4_snmp/python_script/snmp_v2_2_set.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
  - `from pathlib import Path`
  - `sys`
  - `from snmp_v2_3_getbulk import snmpv2_getbulk`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_set (async)(ip, community, oid, value, port)`
  - `get_if_oid(ip, community, if_name)` — 根据接口名称获取接口管理状态OID
  - `shutdown_if(ip, community, if_name, op)`

### `protocol2026/net_4_snmp/python_script/snmp_v2_3_getbulk.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
  - `from pprint import pprint`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_getbulk (async)(ip, community, oid, count, port)`

### `protocol2026/net_4_snmp/python_script/snmp_v2_4_get_all.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `from pathlib import Path`
  - `sys`
  - `from net_4_snmp.python_script.snmp_v2_1_get import snmpv2_get`
  - `from net_4_snmp.python_script.snmp_v2_3_getbulk import snmpv2_getbulk`
  - `asyncio`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv2_get_all(ip_address, community)`

### `protocol2026/net_4_snmp/python_script/snmp_v2_5_trap_server.py`

- **概述**: 简单的SNMPv2陷阱服务器（基于pysnmp库）
- **启发式常量**: `DEFAULT_TRAP_PORT`, `LISTEN_ADDRESS`
- **依赖 (import)**:
  - `asyncio`
  - `sys`
  - `pprint`
  - `argparse`
  - `from pysnmp.hlapi import *`
  - `from pysnmp.entity import engine,config`
  - `from pysnmp.carrier.asyncio.dgram import udp`
  - `from pysnmp.entity.rfc3413 import ntfrcv`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `parse_arguments()` — 解析SNMP陷阱服务器的命令行参数。
  - `cb_fun(snmp_engine, stateReference, contextEngineId, contextName, varBinds, cbCtx)` — SNMP陷阱接收回调函数。每当接收到陷阱时都会调用此函数。
  - `run_trap_receiver (async)()` — 设置并运行异步SNMP陷阱接收器。
  - `main()` — 初始化并运行SNMP陷阱接收器的主函数。

### `protocol2026/net_4_snmp/python_script/snmp_v3_1_get.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv3_get (async)(ip, username, auth_key, priv_key, oid, auth_protocol, priv_protocol, port)`

### `protocol2026/net_4_snmp/python_script/snmp_v3_2_set.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
  - `from snmp_v3_3_getbulk import snmpv3_getbulk`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv3_set (async)(ip, username, auth_key, priv_key, oid, value, auth_protocol, priv_protocol, port)`
  - `get_if_oid(ip, username, auth_key, priv_key, if_name)` — 根据接口名称获取接口管理状态OID
  - `shutdown_if(ip, username, auth_key, priv_key, if_name, op)`

### `protocol2026/net_4_snmp/python_script/snmp_v3_3_getbulk.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv3_getbulk (async)(ip, username, auth_key, priv_key, oid, count, auth_protocol, priv_protocol, port)`

### `protocol2026/net_4_snmp/python_script/snmp_v3_4_get_all.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **依赖 (import)**:
  - `asyncio`
  - `from pathlib import Path`
  - `sys`
  - `from snmp_v3_1_get import snmpv3_get`
  - `from snmp_v3_3_getbulk import snmpv3_getbulk`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `snmpv3_get_all(ip_address, username, auth_key, priv_key)`

### `protocol2026/net_4_snmp/python_script/snmp_v3_5_trap_server.py`

- **概述**: SNMP v2/v3 示例：GET/SET/GETBULK/全表/TRAP
- **启发式常量**: `DEFAULT_LISTEN_ADDRESS`, `DEFAULT_TRAP_PORT`
- **依赖 (import)**:
  - `asyncio`
  - `pprint`
  - `sys`
  - `from pysnmp.hlapi.v3arch.asyncio import *`
  - `from pysnmp.entity import engine,config`
  - `from pysnmp.carrier.asyncio.dgram import udp`
  - `from pysnmp.entity.rfc3413 import ntfrcv`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `cb_fun(snmp_engine, state_reference, context_engine_id, context_name, var_binds, cb_ctx)` — SNMPv3 Trap 接收回调函数
  - `run_trap_receiver (async)(listen_address, trap_port, username, auth_key, priv_key, auth_protocol, priv_protocol)` — 运行 SNMPv3 Trap 接收器
  - `main()` — 主函数

### `protocol2026/net_5_syslog/__init__.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_5_syslog/nexus_syslog_example.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **启发式常量**: `PORT_LIST`
- **依赖 (import)**:
  - `from cli import *`
  - `from nxos import *`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `IFMBR_check(ints, asic, slice, N)`

### `protocol2026/net_5_syslog/syslog/__init__.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_5_syslog/syslog/syslog_client.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **依赖 (import)**:
  - `socket`
- **类**:
  - **`Facility`**（基类: `object`）
  - **`Level`**（基类: `object`）
  - **`Syslog`**（基类: `object`）
    - `__init__(self, host, port, facility)`
    - `send(self, message, level)`
    - `warn(self, message)`
    - `notice(self, message)`
    - `error(self, message)`
- **模块级函数**: （无）

### `protocol2026/net_5_syslog/syslog/syslog_server_to_file.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **依赖 (import)**:
  - `logging`
  - `socketserver`
  - `re`
  - `from pathlib import Path`
  - `sys`
  - `from net_4_snmp.python_script.snmp_v2_2_set import shutdown_if`
- **类**:
  - **`SyslogUDPHandler`**（基类: socketserver.BaseRequestHandler）
    - `handle(self)`
- **模块级函数**: （无）

### `protocol2026/net_5_syslog/syslog_write_db/__init__.py`

- **概述**: Syslog 发送/落盘/服务端入库
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_5_syslog/syslog_write_db/orm_1_syslog_create_table.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import declarative_base`
  - `from sqlalchemy import Column,String,Integer,DateTime`
  - `datetime`
  - `os`
- **类**:
  - **`Syslog`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `protocol2026/net_5_syslog/syslog_write_db/orm_2_syslog_server_to_db.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `from pathlib import Path`
  - `sys`
  - `socketserver`
  - `re`
  - `from dateutil import parser`
  - `from sqlalchemy.orm import sessionmaker`
  - `from sqlalchemy import create_engine`
  - `from net_5_syslog.syslog_write_db.orm_1_syslog_create_table import Syslog,db_file_name`
- **类**:
  - **`SyslogUDPHandler`**（基类: socketserver.BaseRequestHandler）
    - `handle(self)`
- **模块级函数**: （无）

### `protocol2026/net_5_syslog/syslog_write_db/orm_3_syslog_show.py`

- **概述**: SQLAlchemy ORM：建表/写库/读库/展示
- **依赖 (import)**:
  - `from pathlib import Path`
  - `sys`
  - `os`
  - `from matplotlib import pyplot as plt`
  - `from sqlalchemy.orm import sessionmaker`
  - `from sqlalchemy import create_engine`
  - `from net_5_syslog.syslog_write_db.orm_1_syslog_create_table import Syslog,db_file_name`
  - `from sqlalchemy import func`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `syslog_show()`

### `protocol2026/net_6_tcp/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_6_tcp/socket_server/__init__.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_6_tcp/socket_server/socket_client_from_input.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - `from socket import *`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_6_tcp/socket_server/socket_client_from_list.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - `from socket import *`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_6_tcp/socket_server/socket_server.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - `from socket import *`
  - `from datetime import datetime`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_6_tcp/socket_server_json/__init__.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_6_tcp/socket_server_json/socket_client_json.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - `json`
  - `from socket import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `client_json(ip, port, obj)`

### `protocol2026/net_6_tcp/socket_server_json/socket_server_json.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - `json`
  - `from socket import *`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `server_json(ip, port)`

### `protocol2026/net_6_tcp/socket_server_pickle/__init__.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_6_tcp/socket_server_pickle/socket_client_pickle.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - `from io import BytesIO`
  - `from socket import socket,AF_INET,SOCK_STREAM`
  - `pickle`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `client_pickle(ip, port, obj)`

### `protocol2026/net_6_tcp/socket_server_pickle/socket_server_pickle.py`

- **概述**: TCP 套接字服务端/客户端
- **依赖 (import)**:
  - `from socket import *`
  - `pickle`
  - `struct`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `server_pickle(ip, port)`

### `protocol2026/net_7_telnet/asyncio_netmiko.py`

- **概述**: Telnet 或 asyncio+Netmiko
- **启发式常量**: `CSR`
- **依赖 (import)**:
  - `asyncio`
  - `os`
  - `threading`
  - `sys`
  - `from pathlib import Path`
  - `from net_8_ssh.netmiko_plan.netmiko_1_show_client import netmiko_show_cred`
  - `from datetime import datetime`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `async_netmiko (async)(task_id, ip, username, password, cmd)`

### `protocol2026/net_7_telnet/netmiko_telnet_ssh.py`

- **概述**: Telnet 或 asyncio+Netmiko
- **启发式常量**: `CSR1`
- **依赖 (import)**:
  - `from netmiko import Netmiko`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_7_telnet/simple_telnet_client.py`

- **概述**: Telnet 或 asyncio+Netmiko
- **依赖 (import)**:
  - `from telnetlib import Telnet`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `telnet_client(ip, username, password, cmd_list, enable, verbose)`

### `protocol2026/net_8_ssh/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/__init__.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/config_bak_and_diff/__init__.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/config_bak_and_diff/config_diff_1_create_table.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import declarative_base`
  - `from sqlalchemy import Column,String,Integer,DateTime`
  - `datetime`
  - `os`
  - `from pathlib import Path`
- **类**:
  - **`RouterConfig`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/config_bak_and_diff/config_diff_2_dff_conf.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from difflib import Differ`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `diff_file(file1, file2)`
  - `diff_txt(txt1, txt2)`

### `protocol2026/net_8_ssh/netmiko_plan/config_bak_and_diff/config_diff_3_get_md5_config.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `sys`
  - `from pathlib import Path`
  - `from net_8_ssh.netmiko_plan.config_bak_and_diff.config_diff_1_create_table import RouterConfig,db_file_path`
  - `from net_8_ssh.netmiko_plan.netmiko_1_show_client import netmiko_show_cred,device_ip,username,password`
  - `re`
  - `hashlib`
  - `from datetime import datetime`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_md5_config(host, username, password)`

### `protocol2026/net_8_ssh/netmiko_plan/config_bak_and_diff/config_diff_4_compare_config.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `sys`
  - `from pathlib import Path`
  - `from config_diff_2_dff_conf import diff_txt`
  - `from config_diff_1_create_table import RouterConfig,db_file_path`
  - `from sqlalchemy.orm import sessionmaker`
  - `from sqlalchemy import func`
  - `from sqlalchemy import create_engine`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `def_config_id()`

### `protocol2026/net_8_ssh/netmiko_plan/excel_tools/__init__.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/excel_tools/excel_opts_1_create.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `pandas as pd`
  - `yaml`
  - `os`
  - `from pathlib import Path`
  - `from pprint import pprint`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `excel_create(yaml_file)`

### `protocol2026/net_8_ssh/netmiko_plan/excel_tools/excel_opts_2_insert.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `pandas as pd`
  - `from pprint import pprint`
  - `sys`
  - `from pathlib import Path`
  - `from excel_opts_1_create import excel_dir,excel_file_path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `generate_cmd(row)`
  - `excel_insert(excel_file)`

### `protocol2026/net_8_ssh/netmiko_plan/jinja2_dir/jinja2_python.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from jinja2 import Template`
  - `yaml`
  - `from pprint import pprint`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_0_basic.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from netmiko import Netmiko`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_1_show_client.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from netmiko import Netmiko`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_show_cred(host, username, password, cmd, device_type, use_textfsm, ssh_port)`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_2_ntc_template_1_basic.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `os`
  - `from textfsm import clitable`
  - `sys`
  - `from pathlib import Path`
  - `from netmiko_1_show_client import netmiko_show_cred,device_ip,username,password`
  - `from ntc_templates.parse import parse_output`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `clitable_to_dict(cli_table)`
  - `netmiko_ntc_template(ip, username, password, cmd, device_type)`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_2_ntc_template_2_async.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `os`
  - `sys`
  - `from pathlib import Path`
  - `from netmiko_1_show_client import netmiko_show_cred`
  - `from netmiko_2_ntc_template_1_basic import clitable_to_dict`
  - `from textfsm import clitable`
  - `yaml`
  - `from pprint import pprint`
  - `from ntc_templates.parse import parse_output`
  - `asyncio`
  - `os`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `async_netmiko_ntc_template (async)(ip, username, password, cmd, device_type, ssh_port)`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_3_config_1_basic.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from netmiko import Netmiko`
  - `yaml`
  - `os`
  - `from jinja2 import Template`
  - `sys`
  - `from pathlib import Path`
  - `from netmiko_1_show_client import device_ip,username,password`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_config_cred(host, username, password, cmds_list, device_type, verbose, ssh_port)`
  - `config_cmd_list(config_direction_name)`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_3_config_2_async.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from netmiko import Netmiko`
  - `yaml`
  - `os`
  - `from jinja2 import Template`
  - `from pprint import pprint`
  - `asyncio`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_config_cred (async)(host, username, password, cmds_list, device_type, enable, verbose, ssh_port)`
  - `_gather_all (async)()`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_3_config_db_0_async_netmiko.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from netmiko import Netmiko`
  - `asyncio`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_config_cred (async)(host, username, password, cmds_list, device_type, enable, verbose, ssh_port)`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_3_config_db_0_create_db.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import declarative_base,relationship`
  - `from sqlalchemy import Column,String,Integer,DateTime,ForeignKey`
  - `datetime`
  - `from pathlib import Path`
  - `os`
- **类**:
  - **`Router`**（基类: Base） — 路由器表：核心表，存储路由器基本信息
    - `to_dict(self)` — 将对象转换为字典，用于Jinja2模板渲染和JSON序列化
    - `__repr__(self)` — 对象的字符串表示，用于日志和调试
  - **`DeviceType`**（基类: Base） — 设备类型表：存储网络设备的类型信息（如cisco_ios, juniper_junos等）
    - `__repr__(self)` — 对象的字符串表示
  - **`LoginCredential`**（基类: Base） — 登录凭证表：存储设备的登录认证信息
    - `__repr__(self)` — 对象的字符串表示
  - **`User`**（基类: Base） — 用户表：存储路由器上配置的用户账号
    - `to_dict(self)` — 将对象转换为字典
    - `__repr__(self)` — 对象的字符串表示
  - **`Interface`**（基类: Base） — 接口表：存储路由器的网络接口信息
    - `to_dict(self)` — 将对象转换为字典
    - `__repr__(self)` — 对象的字符串表示
  - **`CPUUsage`**（基类: Base） — CPU使用率表：存储路由器CPU使用情况的历史记录
    - `__repr__(self)` — 对象的字符串表示
  - **`OSPFProcess`**（基类: Base） — OSPF进程表：存储路由器的OSPF路由进程信息
    - `to_dict(self)` — 将对象转换为字典，包含完整的OSPF配置
    - `__repr__(self)` — 对象的字符串表示
  - **`Area`**（基类: Base） — OSPF区域表：存储OSPF进程中配置的区域信息
    - `__repr__(self)` — 对象的字符串表示
  - **`OSPFNetwork`**（基类: Base） — OSPF网络表：存储OSPF区域中配置的网络信息
    - `__repr__(self)` — 对象的字符串表示，包含完整路径信息
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_3_config_db_1_insert_db.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from sqlalchemy.orm import sessionmaker`
  - `from sqlalchemy import create_engine`
  - `sys`
  - `from pathlib import Path`
  - `from netmiko_3_config_db_0_create_db import Router,Interface,OSPFProcess,Area,OSPFNetwork,db_filename`
  - `from netmiko_3_config_db_0_create_db import User,LoginCredential,DeviceType`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_3_config_db_2_config.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from sqlalchemy.orm import sessionmaker`
  - `from sqlalchemy import create_engine`
  - `sys`
  - `from pathlib import Path`
  - `os`
  - `from jinja2 import Template`
  - `from pprint import pprint`
  - `from netmiko_3_config_db_0_async_netmiko import netmiko_config_cred`
  - `asyncio`
  - `yaml`
  - `from netmiko_3_config_db_0_create_db import Router,Interface,OSPFProcess,Area,OSPFNetwork,db_filename`
  - `from netmiko_3_config_db_0_create_db import User,LoginCredential`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `_gather_all (async)()`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_4_1_from_excel.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `pandas as pd`
  - `sys`
  - `from pathlib import Path`
  - `from netmiko_1_show_client import device_ip,username,password`
  - `from netmiko_3_config_1_basic import netmiko_config_cred`
  - `from excel_tools.excel_opts_2_insert import excel_file_with_cmd`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `config_from_excel(excel_file)`

### `protocol2026/net_8_ssh/netmiko_plan/netmiko_4_2_to_excel.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `sys`
  - `from pathlib import Path`
  - `from netmiko_2_ntc_template_1_basic import netmiko_ntc_template`
  - `from netmiko_1_show_client import device_ip,username,password`
  - `from excel_tools.excel_opts_2_insert import excel_dir`
  - `pandas as pd`
  - `from pprint import pprint`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `display_to_excel(excel_file)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/__init__.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Flask`
  - `from flask_wtf.csrf import CSRFProtect`
  - `from sqlalchemy import create_engine`
  - `from sqlalchemy.orm import sessionmaker,scoped_session`
  - `os`
  - `sys`
  - `from pathlib import Path`
  - `from netmiko_3_config_db_0_create_db import Base,db_filename`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `create_app()`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/app.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `os`
  - `sys`
  - `from pathlib import Path`
  - `importlib.util`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `main()`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/forms.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask_wtf import FlaskForm`
  - `from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField`
  - `from wtforms.validators import DataRequired,IPAddress,ValidationError,InputRequired`
- **类**:
  - **`LoginForm`**（基类: FlaskForm） — 用户登录表单
  - **`DeviceTypeForm`**（基类: FlaskForm） — 设备类型表单
  - **`CredentialForm`**（基类: FlaskForm） — 登录凭证表单
  - **`RouterForm`**（基类: FlaskForm） — 路由器表单
  - **`InterfaceForm`**（基类: FlaskForm） — 接口表单
    - `validate_mask(self, field)` — 验证子网掩码格式
  - **`UserForm`**（基类: FlaskForm） — 路由器用户表单
    - `validate_priv(self, field)` — 验证权限级别在有效范围内
  - **`OSPFProcessForm`**（基类: FlaskForm） — OSPF进程表单
  - **`AreaForm`**（基类: FlaskForm） — OSPF区域表单
    - `validate_area_id(self, field)` — 验证区域ID在有效范围内
  - **`NetworkForm`**（基类: FlaskForm） — OSPF网络表单
    - `validate_wildmask(self, field)` — 验证通配符掩码格式
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/web_front/models/__init__.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from netmiko_3_config_db_0_create_db import Base,Router,DeviceType,LoginCredential,Interface,User,OSPFProcess,Area,OSPFNetwork,db_filename`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/__init__.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from web_front.routes.auth import auth_bp`
  - `from web_front.routes.devicetypes import devicetypes_bp`
  - `from web_front.routes.credentials import credentials_bp`
  - `from web_front.routes.routers import routers_bp`
  - `from web_front.routes.interfaces import interfaces_bp`
  - `from web_front.routes.users import users_bp`
  - `from web_front.routes.ospf import ospf_bp`
  - `from web_front.routes.areas import areas_bp`
  - `from web_front.routes.networks import networks_bp`
  - `from web_front.routes.main import main_bp`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/areas.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import AreaForm`
  - `from web_front.models import Area,OSPFProcess`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `areas(ospf_id)`
  - `add_area(ospf_id)`
  - `edit_area(id)`
  - `delete_area(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/auth.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,session`
  - `from web_front.forms import LoginForm`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `login()`
  - `logout()`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/credentials.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import CredentialForm`
  - `from web_front.models import LoginCredential`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `credentials()`
  - `add_credential()`
  - `edit_credential(id)`
  - `delete_credential(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/devicetypes.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import DeviceTypeForm`
  - `from web_front.models import DeviceType`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `devicetypes()`
  - `add_devicetype()`
  - `edit_devicetype(id)`
  - `delete_devicetype(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/interfaces.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import InterfaceForm`
  - `from web_front.models import Interface,Router`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `interfaces(router_id)`
  - `add_interface(router_id)`
  - `edit_interface(id)`
  - `delete_interface(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/main.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template`
  - `from web_front.utils import login_required`
  - `from web_front.models import Router,DeviceType,LoginCredential,Interface,User,OSPFProcess`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `index()`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/networks.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import NetworkForm`
  - `from web_front.models import OSPFNetwork,Area`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `networks(area_id)`
  - `add_network(area_id)`
  - `edit_network(id)`
  - `delete_network(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/ospf.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import OSPFProcessForm`
  - `from web_front.models import OSPFProcess,Router`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ospf(router_id)`
  - `add_ospf(router_id)`
  - `edit_ospf(id)`
  - `delete_ospf(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/routers.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import RouterForm`
  - `from web_front.models import Router,LoginCredential,DeviceType`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `routers()`
  - `add_router()`
  - `edit_router(id)`
  - `delete_router(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/routes/users.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import Blueprint,render_template,redirect,url_for,flash,current_app`
  - `from web_front.utils import login_required`
  - `from web_front.forms import UserForm`
  - `from web_front.models import User,Router`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `users(router_id)`
  - `add_user(router_id)`
  - `edit_user(id)`
  - `delete_user(id)`

### `protocol2026/net_8_ssh/netmiko_plan/web_front/run.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from web_front import create_app`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/netmiko_plan/web_front/utils.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `from flask import session,redirect,url_for,flash`
  - `from functools import wraps`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `login_required(f)`

### `protocol2026/net_8_ssh/netmiko_plan/yaml_dir/yaml_control.py`

- **概述**: Netmiko 基础/模板/配置/异步
- **依赖 (import)**:
  - `yaml`
  - `from pprint import pprint`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/paramiko_plan/__init__.py`

- **概述**: Paramiko SSH 执行命令
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/paramiko_plan/ssh_client_multi_cmd.py`

- **概述**: Paramiko SSH 执行命令
- **依赖 (import)**:
  - `paramiko`
  - `time`
  - `sys`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ssh_client_multi_cmd(ip, username, password, cmd_list, verbose)`

### `protocol2026/net_8_ssh/paramiko_plan/ssh_client_one_cmd.py`

- **概述**: Paramiko SSH 执行命令
- **依赖 (import)**:
  - `paramiko`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ssh_client_one_cmd(ip, username, password, cmd)`

### `protocol2026/net_8_ssh/pyats/pyats_1_netmiko.py`

- **概述**: Cisco pyATS 学习/对比/配置
- **依赖 (import)**:
  - `from netmiko import Netmiko`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_show_cred(host, username, password, cmd, device_type, use_genie, ssh_port)`

### `protocol2026/net_8_ssh/pyats/pyats_2_learn/pyats_2_learn_1_load_top_file.py`

- **概述**: Cisco pyATS 学习/对比/配置
- **依赖 (import)**:
  - `from pyats.topology import loader`
  - `from pprint import pprint`
  - `from pathlib import Path`
  - `os`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/pyats/pyats_2_learn/pyats_2_learn_2_load_list.py`

- **概述**: Cisco pyATS 学习/对比/配置
- **依赖 (import)**:
  - `from genie.testbed import load`
  - `from pprint import pprint`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/pyats/pyats_3_diff/pyats_3_diff_2_python.py`

- **概述**: Cisco pyATS 学习/对比/配置
- **依赖 (import)**:
  - `from deepdiff import DeepDiff`
  - `from pprint import pprint`
  - `json`
  - `from pathlib import Path`
  - `sys`
  - `os`
  - `from pyats_2_learn.pyats_2_learn_2_load_list import testbed`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/pyats/pyats_4_config/pyats_4_config.py`

- **概述**: Cisco pyATS 学习/对比/配置
- **依赖 (import)**:
  - `from genie.libs.conf.interface import Interface`
  - `from pathlib import Path`
  - `sys`
  - `os`
  - `from pyats_2_learn.pyats_2_learn_2_load_list import testbed`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/pyats/pyats_5_job/bgp_job.py`

- **概述**: Cisco pyATS 学习/对比/配置
- **依赖 (import)**:
  - `os`
  - `from pyats.easypy import run`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `main(runtime)` — 作业入口点

### `protocol2026/net_8_ssh/pyats/pyats_5_job/bgp_test.py`

- **概述**: Cisco pyATS 学习/对比/配置
- **依赖 (import)**:
  - `logging`
  - `from pyats import aetest`
  - `from genie.testbed import load as tbload`
  - `from pyats.topology import Testbed`
  - `yaml`
- **类**:
  - **`CommonSetup`**（基类: aetest.CommonSetup） — 公共设置部分
    - `connect(self, testbed)` — 连接到所有设备
  - **`BGPNeighborsEstablished`**（基类: aetest.Testcase） — BGP邻居建立状态测试
    - `setup(self)` — 从测试设备中获取并保存BGP详细信息
    - `test_bgp_neighbors(self)` — 检查BGP邻居状态
  - **`BGPRouteCheck`**（基类: aetest.Testcase） — BGP邻居建立状态测试
    - `setup(self)` — 从测试设备中获取并保存BGP详细信息
    - `test_bgp_routes(self)` — 检查BGP路由
  - **`CommonCleanup`**（基类: aetest.CommonCleanup） — 公共清理部分
    - `disconnect(self, testbed)` — 断开所有设备连接
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/pyats/pytest/pytest_ospf.py`

- **概述**: pytest 封装网络检查
- **依赖 (import)**:
  - `pytest`
  - `from netmiko import Netmiko`
  - `os`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `netmiko_show_cred(ospf_router)`
  - `test_ospf_neigh_1()`
  - `test_ospf_neigh_2()`

### `protocol2026/net_8_ssh/pyats/pytest/pytest_ping.py`

- **概述**: ICMP ping 单主机/扫描/IPv6
- **依赖 (import)**:
  - `pytest`
  - `pythonping`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ping(target, count)`
  - `test_ping_1()`
  - `test_ping_2()`

### `protocol2026/net_8_ssh/sftp_plan/__init__.py`

- **概述**: FTP 列目录/上传/下载/查找
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_8_ssh/sftp_plan/sftp_client.py`

- **概述**: FTP 列目录/上传/下载/查找
- **依赖 (import)**:
  - `paramiko`
  - `os`
  - `sys`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ssh_sftp_put(ip, user, password, local_file, remote_file, port)`
  - `ssh_sftp_get(ip, user, password, remote_file, local_file, port)`

### `protocol2026/net_9_ftp/file_dir/qytang2.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/net_9_ftp/ftp_find.py`

- **概述**: FTP 列目录/上传/下载/查找
- **依赖 (import)**:
  - `from ftplib import FTP`
  - `re`
  - `optparse`
  - `os`
  - `sys`
  - `from pathlib import Path`
  - `from tools.decorator_time import print_run_time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ftp_find(hostname, username, password, start_dir, file_type, verbose)`

### `protocol2026/net_9_ftp/ftp_get.py`

- **概述**: FTP 列目录/上传/下载/查找
- **依赖 (import)**:
  - `ftplib`
  - `os`
  - `os`
  - `sys`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `downloadfile(hostname, file, username, password, rdir, ldir, verbose)`

### `protocol2026/net_9_ftp/ftp_list.py`

- **概述**: FTP 列目录/上传/下载/查找
- **依赖 (import)**:
  - `ftplib`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `listftpfile(hostname, username, password, remote_dir, verbose)`

### `protocol2026/net_9_ftp/ftp_put.py`

- **概述**: FTP 列目录/上传/下载/查找
- **依赖 (import)**:
  - `ftplib`
  - `os`
  - `sys`
  - `from pathlib import Path`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `putfile(hostname, file, username, password, rdir, ldir, verbose)`

### `protocol2026/tools/__init__.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `protocol2026/tools/change_ip_to_bytes.py`

- **概述**: IP 转字节
- **依赖 (import)**:
  - `struct`
  - `re`
  - `socket`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `change_ip_to_bytes(IP)`

### `protocol2026/tools/change_mac_to_bytes.py`

- **概述**: MAC 转字节
- **依赖 (import)**:
  - `struct`
  - `re`
  - `binascii`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `change_mac_to_bytes(mac)`

### `protocol2026/tools/checksum.py`

- **概述**: 校验和工具
- **依赖 (import)**:
  - `struct`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `do_checksum(source_bin)`

### `protocol2026/tools/decorator_time.py`

- **概述**: 装饰器工具
- **依赖 (import)**:
  - `from functools import wraps`
  - `from datetime import datetime`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `print_run_time()`

### `protocol2026/tools/get_ifname.py`

- **概述**: 接口名工具
- **依赖 (import)**:
  - `platform`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_ifname(ifname)`

### `protocol2026/tools/get_ip_netifaces.py`

- **概述**: 网卡 IP 获取
- **依赖 (import)**:
  - `from netifaces import ifaddresses,AF_INET,AF_INET6`
  - `from pprint import pprint`
  - `platform`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_ip_address(ifname)`
  - `get_ipv6_address(ifname)`

### `protocol2026/tools/get_mac_netifaces.py`

- **概述**: 网卡 MAC 获取
- **依赖 (import)**:
  - `netifaces`
  - `platform`
  - `pprint`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_mac_address(ifname)`

### `protocol2026/tools/scapy_iface.py`

- **概述**: Scapy 处理 pcap/协议字段/实验
- **依赖 (import)**:
  - `from scapy.all import *`
  - `from tools.get_ifname import get_ifname`
  - `platform`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `scapy_iface(os_name)`

### `protocol2026/tools/sort_ip.py`

- **概述**: IP 排序工具
- **依赖 (import)**:
  - `from socket import inet_aton`
  - `struct`
  - `ipaddress`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `sort_ip(ips)`

### `protocol2026/tools/win_ifname.py`

- **概述**: Windows 接口名
- **依赖 (import)**:
  - `netifaces as ni`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_connection_name_from_guid(iface_guids)`
  - `win_from_name_get_id(ifname)`

### `python基础作业/20260321/3.py`

- **概述**: 创建一个Python脚本，打印一台网络设备的基本信息
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260321/4.py`

- **概述**: 创建一个随机产生IP地址的代码
- **依赖 (import)**:
  - `random`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260321/5.py`

- **概述**: 打印一张简单的IP地址规划表
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260323/1.py`

- **概述**: 定义以下变量，使用 f-string 打印一条网络设备的Syslog告警信息:
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260323/2.py`

- **概述**: 现在有一个接口名字符串:
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260323/3.py`

- **概述**: 从设备采集回来的版本信息字符串经常有多余的空格，需要处理后再使用:
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260323/4.py`

- **概述**: 定义以下变量，使用 format() 打印一份格式整齐的接口状态报告:
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260324/1.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `re`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260324/2.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `re`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260325/1.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `os`
  - `re`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260326/1.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `os`
  - `re`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260326/2.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260327/1.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `re`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260327/2.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260330/1.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `os`
  - `shutil`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/20260402/save_int_info.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from day08_20260331.day08_task02_ping_gateway import ping_check`
  - `from day09_20260401.day09_task01_ssh_gateway import ssh_run`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `collect_interface_info(device_list)`

### `python基础作业/day08_20260331/1.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `os`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/day08_20260331/day08_task02_ping_gateway.py`

- **概述**: ICMP ping 单主机/扫描/IPv6
- **依赖 (import)**:
  - `from pythonping import ping`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ping_check(host)`

### `python基础作业/day08_20260331/my_server.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `from http.server import HTTPServer,CGIHTTPRequestHandler`
- **类**: （无模块级类定义）
- **模块级函数**: （无）

### `python基础作业/day09_20260401/day09_task01_ssh_gateway.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `re`
  - `paramiko`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ssh_run(host, username, password, command)`

### `python基础作业/day10_20260403/day10_task1_cfg_change.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `sys`
  - `os`
  - `hashlib`
  - `time`
  - `re`
  - `from day09_20260401.day09_task01_ssh_gateway import ssh_run`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `get_device_config(ip, username, password)` — SSH登录思科路由器执行show running-config，
  - `monitor_config_change(ip, username, password)` — 每5秒获取设备配置，计算MD5值，检测配置是否变化

### `python基础作业/day12_20260406/day12_task1_multicmd.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `paramiko`
  - `time`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `qytang_multicmd(ip, username, password, cmd_list, enable, wait_time, verbose)` — 参数说明：

### `python基础作业/day13_20260407/day13_task1.py`

- **概述**: 网络设备接口配置管理脚本
- **依赖 (import)**:
  - `sys`
  - `os`
  - `from day12_20260406.day12_task1_multicmd import qytang_multicmd`
- **类**:
  - **`Interface`**（基类: `object`） — 接口配置类，只保存接口数据
    - `__init__(self, name)`
    - `__str__(self)` — 格式化打印接口信息
  - **`NetworkDevice`**（基类: `object`） — 网络设备类，保存设备登录信息及关联的接口
    - `__init__(self, ip, username, password)`
    - `add_interface(self, interface)` — 将接口加入本设备，并建立双向关联
    - `apply(self)` — 将所有关联接口的配置一次性下发到设备
    - `__str__(self)` — 打印设备信息及下属接口列表
- **模块级函数**: （无）

### `python基础作业/day14_20260408/day14_task01_backup.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `os`
  - `time`
  - `from datetime import datetime,timedelta`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `main()`

### `python基础作业/day14_20260408/day14_task02_ssh_argparse.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `argparse`
  - `paramiko`
- **类**: （无模块级类定义）
- **模块级函数**:
  - `ssh_run(host, username, password, command)` — 通过 paramiko 执行 SSH 命令并返回结果
  - `main()`

### `python基础作业/day15_20260409/day15_task01.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `datetime`
  - `from sqlalchemy import create_engine,Column,Integer,String,DateTime`
  - `from sqlalchemy.orm import declarative_base,sessionmaker`
- **类**:
  - **`Device`**（基类: Base）
    - `__repr__(self)`
- **模块级函数**: （无）

### `python基础作业/day16_20260410/day16_task01.py`

- **概述**: 学员作业/任务脚本
- **依赖 (import)**:
  - `sys`
  - `os`
  - `hashlib`
  - `time`
  - `datetime`
  - `re`
  - `from day12_20260406.day12_task1_multicmd import qytang_multicmd`
  - `from sqlalchemy import create_engine,Column,Integer,String,DateTime`
  - `from sqlalchemy.orm import declarative_base,sessionmaker`
- **类**:
  - **`RouterConfig`**（基类: Base） — 路由器配置备份模型
    - `__repr__(self)`
- **模块级函数**:
  - `get_show_run(host, username, password)` — 获取配置并计算 hash
  - `save_config(host, config, config_hash)` — 写入数据库（使用独立 session，避免事务残留）
  - `get_latest_two_hashes(host)` — 查询最近两条记录

### `test.py`

- **概述**: 课件或练习用 Python 脚本
- **依赖 (import)**:
  - （无顶层 import）
- **类**: （无模块级类定义）
- **模块级函数**: （无）

---

## 3. 关键代码模式与模板

### 3.1 文件头与版权注释

课件 `.py` 普遍使用：

```text
#!/usr/bin/env python3
# -*- coding=utf-8 -*-   或 coding: utf-8 -*-
# 本脚由亁颐堂… 用于亁颐堂NetDevOps课程 / 乾颐盾Python课程
# 教主QQ、官网、VIP 链接…
```

**含义**：强调课程归属与 VIP 资源；作业脚本常简化为 `utf-8` + 任务中文说明。

### 3.2 计时装饰器（高频）

- 三层嵌套：`def outer(): def decorator(f): @wraps(f) def inner(*args,**kwargs): ... return inner; return decorator`。
- `functools.wraps` 保留原函数 `__name__` / 文档。
- 典型用途：ARP 扫描、SNMP 轮询、批量 Netmiko 等前后打印耗时。
- 参考：`protocol2026/net_1_arp/time_decorator.py`（`run_time()`）、`protocol2026/tools/decorator_time.py`（`print_run_time()`）。

### 3.3 `if __name__ == '__main__':`

- 课件中大量脚本以「可直接运行」为目标：`__main__` 内写演示参数、单测路由、或 `pass` 占位。
- 作业（Day4–6）在 `__main__` 里写 **设备 IP、community、数据库路径、InfluxDB 主机** 等，便于 `crontab` 调用。

### 3.4 网络 I/O 模式

| 模式 | 典型库/API | 课件位置 |
| --- | --- | --- |
| 原始套接字 TCP/UDP | `socket` | `net_3_udp`, `net_6_tcp/socket_server*` |
| 序列化对话 | `json` / `pickle` 与自定义长度前缀 | `socket_server_json`, `socket_server_pickle` |
| SSH/Telnet 设备 | `netmiko.ConnectHandler`、异步 `asyncio` | `net_7_telnet`, `net_8_ssh/netmiko_plan` |
| 底层 SSH | `paramiko` | `net_8_ssh/paramiko_plan` |
| 结构化测试 | `pyATS`、`pytest` | `net_8_ssh/pyats` |
| 抓包/离线分析 | `scapy`、`pyshark` | `net_13_traffic_analysis` |
| SNMP | `pysnmp` 异步 hlapi | `net_4_snmp/python_script`, 作业 `day6_snmp_*` |
| 邮件 | `smtplib`、`poplib`、`imaplib`、`mailparser` | `net_10_smtp`, `net_11_pop3` |
| 目录服务 | `ldap3` | `net_12_ldap` |
| FTP | `ftplib` | `net_9_ftp` |

### 3.5 数据库与持久化

- **SQLAlchemy ORM**：`declarative_base()`（或 2.0 风格 `DeclarativeBase`）、`Column`、`sessionmaker`、`create_engine`；典型三步：**建表脚本** → **采集写库** → **读库 + 可视化**（Pygal/Bokeh）。
- **InfluxDB 1.x**：`influxdb.InfluxDBClient`，`points` 含 `measurement`、`tags`、`fields`、`time`。
- **MongoDB**：`pymongo` + 聚合管道，见于 NetFlow Mongo 版本。

### 3.6 Web（Flask）

- **Blueprint**：`routes/*.py` 按资源拆分（`users`、`routers`、`interfaces`…）。
- **WTForms**：`forms.py` 定义表单类，路由中校验。
- **Flask-Login / SQLAlchemy**：`models` + `utils` 工具函数，`run.py` 启动。

### 3.7 类型标注与命名

- 课件以 **运行时教学** 为主，**类型标注不强制**；出现时常在较新脚本或作业中。
- 命名：**小写+下划线** 函数/变量；**驼峰** 较少；类名 **PascalCase**（如 Scapy 实验中的 Telnet 相关 class）。
- 注释：**中文讲解 + 英文关键词** 混排，关键步骤用 `# ~~~` 或分段标题。

---

## 4. 跨文件调用关系

### 4.1 非 Python import 的「逻辑复用」

课件大量脚本是 **独立可运行** 的，**跨文件 import 较少**；复用主要靠：复制装饰器、复制 ORM 模型模式、同一目录下 `yaml`/`excel` 数据驱动。

### 4.2 包内 import（相对/绝对）

| 区域 | 典型关系 |
| --- | --- |
| `net_8_ssh/netmiko_plan/web_front` | `app` 注册 `routes.*` Blueprint；`forms` / `models` / `utils` 被路由引用 |
| `net_13_traffic_analysis/python_netflow/new_mongodb_version` | `reporter_app` → `mongo_config`、`netflow_parser_v9` |
| `net_13_traffic_analysis/python_netflow/new_orm_version` | `netflow_orm_3_collector_main` 依赖 ORM 模块与表定义 |
| `NetDevOps作业/day6` | `day6_2` / `day6_4` 通过 `sys.path` 插入后 `from code.tools.day6_snmp_getbulk import ...`；`day6_snmp_get_all` 聚合调用 `snmpv2_getbulk` |
| `protocol2026/net_4_snmp/airflow/dags` | 多个 DAG 文件并列，依赖 Airflow、`netmiko`、自建 ORM 脚本 |

### 4.3 常用第三方库（跨课件）

`netmiko`, `paramiko`, `scapy`, `pysnmp`, `sqlalchemy`, `flask`, `ldap3`, `pyshark`, `influxdb`, `openpyxl`, `jinja2`, `matplotlib`/`bokeh`/`pygal`, `pyats`, `pytest`, `ftplib`, `smtplib` 等。

---

## 5. 作业速查清单

### 5.1 NetDevOps 作业（按天）

| 天数 | 核心能力 | 关键文件 |
| --- | --- | --- |
| Day1 | 基础脚本 | `day1_20260413_task1.py` |
| Day2 | UDP 客户端/服务端自测 | `udp_client_test.py`, `udp_server_test.py` |
| Day3 | SSH 单命令 + Bokeh 饼图/NetFlow 图 | `day3_ssh_single_cmd.py`, `day3_bokeh_bing.py`, `2026_day3_bokeh_netflow.py` |
| Day4 | SQLite ORM + SNMP CPU/内存 + Bokeh + crond | `day4_1_create_db.py` ~ `day4_3`, `tools/day4_get.py`, `day4_bokeh_*.py` |
| Day5 | InfluxDB + 多路由器 SNMP | `day5_1_influxdb_monitor.py`, `tools/day5_get.py` |
| Day6 | GETBULK 接口速率 + SQLite + Bokeh + InfluxDB 并行 | `day6_1`~`day6_4`, `tools/day6_snmp_getbulk.py`, `day6_snmp_get_all.py`, `day6_bokeh_line.py` |

### 5.2 按功能分类速查

| 功能 | 作业/课件入口 | 易错点/备注 |
| --- | --- | --- |
| 文件读写 | 各 `orm_*`、`syslog_server_to_file` | Windows/Linux 路径；`encoding='utf-8'` |
| SQLite + ORM | `day4_*`, `day6_1`~`3`, 课件 `orm_1_create_table` | 引擎 URL `sqlite:///./xxx.db`；`declarative_base` 版本差异 |
| InfluxDB | `day5_1`, `day6_4`, 课件 `influxdb_monitor_router` | **容器内** Grafana 数据源 URL 用服务名非 `127.0.0.1`；`pip install influxdb` |
| SNMP | `day4_get`, `day5_get`, `day6_snmp_*` | Community、OID、`pysnmp` 异步 `asyncio.run`；接口索引对齐 |
| Bokeh | `day4_bokeh_*`, `day6_bokeh_line`, `day3_bokeh_bing` | `output_file`、`figure`、`line`/`vbar`、数据源列名一致 |
| 网络请求/套接字 | Day2 UDP、课件 TCP/UDP | 防火墙、`bind` 地址、`struct.pack` 对齐 |
| SSH | `day3_ssh_single_cmd`, 课件 `netmiko`/`paramiko` | `device_type`、`secret`、启用命令 |
| 定时任务 | 作业 README/crontab 示例 | 解释器使用 **venv 绝对路径**；`docker compose` v2 |

### 5.3 Python 基础作业（目录日期）

- `20260321`–`20260330`、`day08`–`day16`：循环、函数、文件、面向对象、Ping、SSH 网关、配置下发、多命令 SSH、备份、`argparse` 等。
- 根目录 `test.py`、`new.py`：零散练习，需打开具体文件确认题目。

---

## 6. 从代码推断的规范与偏好

1. **编码**：统一 UTF-8；Shebang `#!/usr/bin/env python3`。
2. **缩进**：4 空格；课件极少混用 Tab。
3. **教学顺序**：**协议原理演示**（ARP/ICMP/UDP）→ **Socket** → **SNMP/Syslog** → **TCP 应用** → **远程管理（Telnet/SSH）** → **邮件/LDAP/FTP** → **流量分析** → **综合自动化（Netmiko + DB + Web + Airflow）**。
4. **注释**：**中文**为主，关键英文术语保留；强调「乾颐堂 / 现任明教教主」品牌与 VIP 链接。
5. **实战倾向**：可运行脚本 > 纯理论；设备 IP、community、数据库文件名在 `__main__` 或全局常量中**写死示例**，学员改为实验环境。
6. **可视化**：ORM 查询结果 → **Pygal** 或 **Bokeh** 折线/柱状；NetFlow 有 **Mongo + HTML 报表** 路线。
7. **安全与合规提示**：Scapy 部分涉及 RST、SYN 等，课件用于**实验环境**演示；作业强调 crontab 与 Docker 运维场景。
8. **评分隐含信号**（推断）：脚本能直接运行、路径与依赖说明清楚、**任务编号与 README 对齐**、图表能反映真实采集数据。

---

*文档由自动化扫描与人工归纳生成于工作区；函数体业务逻辑以索引中的签名为纲，细节仍以源文件为准。*
