#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# ORM 导入
from sqlalchemy.orm import sessionmaker
from day7_1_create_db import Router, engine
# Netmiko 配置工具
from tools.ssh_client_netmiko import netmiko_config_cred
# 协程相关
import asyncio
import os
import threading
import pprint
# Jinja2 模板
from jinja2 import Template
# 模板目录（基于脚本自身路径，避免工作目录问题）
base_dir = os.path.dirname(os.path.abspath(__file__))
tem_path = base_dir + '/templates/'
# 读取接口配置模板
with open(tem_path + 'cisco_ios_interface.template', encoding='utf-8') as f:
    interface_config_template = Template(f.read())
# 读取 OSPF 配置模板
with open(tem_path + 'cisco_ios_ospf.template', encoding='utf-8') as f:
    ospf_config_template = Template(f.read())
# 创建协程事件循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
async def async_netmiko(task_id, ip, username, password, cmds_list):
    """在线程池中异步执行 Netmiko 配置推送，并打印任务开始/结束状态。"""
    print(f'ID: {task_id} Started')
    print(os.getpid(), threading.current_thread().ident)
    # run_in_executor 把同步 netmiko 丢到线程池执行
    result = await loop.run_in_executor(None, netmiko_config_cred, ip, username, password, cmds_list)
    print(f'ID: {task_id} Stopped')
    return result
# 连接数据库
Session = sessionmaker(bind=engine)
session = Session()
# 任务计数器与任务列表
task_no = 1
tasks = []
# 查询所有路由器
all_routers = session.query(Router).all()
for router in all_routers:
    router_final_config_list = []
    router_ip = router.ip
    login_username = router.username
    login_password = router.password
    # 组装接口配置列表
    interface_config_list = []
    for interface in router.interface:
        interface_config_list.append({"interface_name": interface.interface_name,
                                      "interface_ip": interface.ip,
                                      "interface_mask": interface.mask
                                      })
    pprint.pprint(interface_config_list)
    # 渲染接口配置模板 → 切分成命令列表
    interface_config_result = interface_config_template.render(interface_list=interface_config_list)
    router_final_config_list.extend(interface_config_result.split('\n'))
    # 提取 OSPF 配置
    router_ospf_process = router.ospf_process
    router_ospf_process_id = router_ospf_process.processid
    router_id = router_ospf_process.routerid
    ospf_dict = {"ospf_process_id": router_ospf_process_id,
                 "router_id": router_id}
    # 组装 OSPF 网络宣告列表
    ospf_network_list = []
    for area in router_ospf_process.area:
        ospf_area_id = area.area_id
        for ospf_network in area.ospf_network:
            ospf_network_list.append({"area": ospf_area_id,
                                      "network": ospf_network.network,
                                      "wildmask": ospf_network.wildmask
                                      })
    ospf_dict["ospf_network_list"] = ospf_network_list
    pprint.pprint(ospf_dict)
    # 渲染 OSPF 配置模板 → 追加到最终命令列表
    ospf_config_result = ospf_config_template.render(**ospf_dict)
    router_final_config_list.extend(ospf_config_result.split('\n'))
    # 创建协程任务
    task = loop.create_task(async_netmiko(task_no, router_ip, login_username, login_password, router_final_config_list))
    tasks.append(task)
    task_no += 1
# 并发执行所有协程
loop.run_until_complete(asyncio.wait(tasks))
