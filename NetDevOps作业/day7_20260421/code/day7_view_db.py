#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from sqlalchemy.orm import sessionmaker
from day7_1_create_db import Router, Interface, OSPFProcess, Area, OSPFNetwork, engine
Session = sessionmaker(bind=engine)
session = Session()
all_routers = session.query(Router).all()
for router in all_routers:
    print(f'=== 路由器: {router.router_name} (IP: {router.ip}) ===')
    print(f'    用户名: {router.username}  密码: {router.password}')
    print(f'    --- 接口 ---')
    for iface in router.interface:
        print(f'        {iface.interface_name}: {iface.ip} / {iface.mask}')
    ospf = router.ospf_process
    if ospf:
        print(f'    --- OSPF 进程 {ospf.processid} (Router-ID: {ospf.routerid}) ---')
        for area in ospf.area:
            print(f'        Area {area.area_id}:')
            for net in area.ospf_network:
                print(f'            network {net.network} {net.wildmask} area {area.area_id}')
    print()
