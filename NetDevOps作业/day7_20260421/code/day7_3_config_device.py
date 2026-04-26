#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from sqlalchemy.orm import sessionmaker
from day7_1_create_db import Router, engine
from tools.ssh_client_netmiko import netmiko_config_cred
import asyncio
import os
import threading
import pprint
from jinja2 import Template
base_dir = os.path.dirname(os.path.abspath(__file__))
tem_path = base_dir + '/templates/'
with open(tem_path + 'cisco_ios_interface.template', encoding='utf-8') as f:
    interface_config_template = Template(f.read())
with open(tem_path + 'cisco_ios_ospf.template', encoding='utf-8') as f:
    ospf_config_template = Template(f.read())
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
async def async_netmiko(task_id, ip, username, password, cmds_list):
    """在线程池中异步执行 Netmiko 配置推送，并打印任务开始/结束状态。"""
    print(f'ID: {task_id} Started')
    print(os.getpid(), threading.current_thread().ident)
    result = await loop.run_in_executor(None, netmiko_config_cred, ip, username, password, cmds_list)
    print(f'ID: {task_id} Stopped')
    return result
Session = sessionmaker(bind=engine)
session = Session()
task_no = 1
tasks = []
all_routers = session.query(Router).all()
for router in all_routers:
    router_final_config_list = []
    router_ip = router.ip
    login_username = router.username
    login_password = router.password
    interface_config_list = []
    for interface in router.interface:
        interface_name = interface.interface_name
        interface_ip = interface.ip
        interface_mask = interface.mask
        interface_config_list.append({"interface_name": interface_name,
                                      "interface_ip": interface_ip,
                                      "interface_mask": interface_mask
                                      })
    pprint.pprint(interface_config_list)
    interface_config_result = interface_config_template.render(interface_list=interface_config_list)
    router_final_config_list.extend(interface_config_result.split('\n'))
    router_ospf_process = router.ospf_process
    router_ospf_process_id = router_ospf_process.processid
    router_id = router_ospf_process.routerid
    ospf_dict = {"ospf_process_id": router_ospf_process_id,
                 "router_id": router_id}
    ospf_network_list = []
    for area in router_ospf_process.area:
        ospf_area_id = area.area_id
        for ospf_network in area.ospf_network:
            ospf_network_net = ospf_network.network
            ospf_network_wildmask = ospf_network.wildmask
            ospf_network_list.append({"area": ospf_area_id,
                                      "network": ospf_network_net,
                                      "wildmask": ospf_network_wildmask
                                      })
    ospf_dict["ospf_network_list"] = ospf_network_list
    pprint.pprint(ospf_dict)
    ospf_config_result = ospf_config_template.render(**ospf_dict)
    router_final_config_list.extend(ospf_config_result.split('\n'))
    task = loop.create_task(async_netmiko(task_no, router_ip, login_username, login_password, router_final_config_list))
    tasks.append(task)
    task_no += 1
loop.run_until_complete(asyncio.wait(tasks))
