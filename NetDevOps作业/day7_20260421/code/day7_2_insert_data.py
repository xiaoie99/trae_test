#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# ORM 导入
from sqlalchemy.orm import sessionmaker
from day7_1_create_db import Router, Interface, OSPFProcess, Area, OSPFNetwork, engine
Session = sessionmaker(bind=engine)
session = Session()
# 设备一接口信息
c8kv1_ifs = [{'ifname': "GigabitEthernet2", 'ip': "172.16.1.1", 'mask': "255.255.255.0"},
             {'ifname': "Loopback0", 'ip': "1.1.1.1", 'mask': "255.255.255.255"}]
# 设备二接口信息
c8kv2_ifs = [{'ifname': "GigabitEthernet2", 'ip': "172.16.1.2", 'mask': "255.255.255.0"},
             {'ifname': "Loopback0", 'ip': "2.2.2.2", 'mask': "255.255.255.255"}]
# 设备一 OSPF 配置
c8kv1_ospf = {"process_id": 1,
              "router_id": "1.1.1.1",
              "areas": [{'area_id': 0, 'networks': [{'ip': "172.16.1.0", 'wildmask': "0.0.0.255"},
                                                    {'ip': "1.1.1.1", 'wildmask': "0.0.0.0"}]}]}
# 设备二 OSPF 配置
c8kv2_ospf = {"process_id": 1,
              "router_id": "2.2.2.2",
              "areas": [{'area_id': 0, 'networks': [{'ip': "172.16.1.0", 'wildmask': "0.0.0.255"},
                                                    {'ip': "2.2.2.2", 'wildmask': "0.0.0.0"}]}]}
# 登录凭据
username = 'admin'
password = 'qwert@12345'
# 汇总后的全量数据
all_network_data = [{'ip': "10.10.1.200",
                     'router_name': 'C8Kv1',
                     'username': username,
                     'password': password,
                     'interfaces': c8kv1_ifs,
                     'ospf': c8kv1_ospf},
                    {'ip': "10.10.1.201",
                     'router_name': 'C8Kv2',
                     'username': username,
                     'password': password,
                     'interfaces': c8kv2_ifs,
                     'ospf': c8kv2_ospf}]
# 清空旧数据后重新插入
session.query(Router).delete()
for device in all_network_data:
    # 创建 Router 条目
    router_device = Router(router_name=device['router_name'],
                           username=device['username'],
                           password=device['password'],
                           ip=device['ip'])
    session.add(router_device)
    # 创建接口条目
    for ifs in device['interfaces']:
        new_if = Interface(router=router_device, interface_name=ifs['ifname'], ip=ifs['ip'], mask=ifs['mask'])
        session.add(new_if)
    # 创建 OSPF 进程条目
    router_device_process = OSPFProcess(router=router_device,
                                        processid=device["ospf"]["process_id"],
                                        routerid=device["ospf"]["router_id"])
    # 创建 Area 及 OSPF 网络条目
    for device_area in device["ospf"]["areas"]:
        router_device_area = Area(ospf_process=router_device_process, area_id=device_area["area_id"])
        session.add(router_device_area)
        for net in device_area["networks"]:
            new_net = OSPFNetwork(area=router_device_area, network=net['ip'], wildmask=net['wildmask'])
            session.add(new_net)
session.commit()
