from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_dir = current_file.parent
sys.path.append(str(current_dir))

from netmiko_3_config_db_0_create_db import Router, Interface, OSPFProcess, Area, OSPFNetwork, db_filename
from netmiko_3_config_db_0_create_db import User, LoginCredential, DeviceType

engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()


# 设备接口信息
c8kv1_ifs = [{'ifname': "GigabitEthernet1", 'ip': "196.21.5.211", 'mask': "255.255.255.0"},
             {'ifname': "GigabitEthernet2", 'ip': "61.128.1.254", 'mask': "255.255.255.0"},
             {'ifname': "Loopback0", 'ip': "1.1.1.1", 'mask': "255.255.255.255"}]

c8kv2_ifs = [{'ifname': "GigabitEthernet1", 'ip': "196.21.5.212", 'mask': "255.255.255.0"},
             {'ifname': "GigabitEthernet2", 'ip': "202.100.1.1", 'mask': "255.255.255.0"},
             {'ifname': "Loopback0", 'ip': "2.2.2.2", 'mask': "255.255.255.255"}]

# 设备登录信息
login_credential = {'credential_name': 'system_admin', 'username': 'admin', 'password': 'Cisc0123'}

# 设备类型
device_type = {'device_type': 'cisco_ios'}

# 设备用户信息
c8kv1_user = [{'username': 'qytuser1', 'password': 'Cisc0123', 'priv': 15},
              {'username': 'qytuser2', 'password': 'Cisc0123', 'priv': 15}]

c8kv2_user = [{'username': 'qytuser11', 'password': 'Cisc0123', 'priv': 15},
              {'username': 'qytuser22', 'password': 'Cisc0123', 'priv': 15}]


# 设备OSPF信息
c8kv1_ospf = {"processid": 1,
              "routerid": "1.1.1.1",
              "areas": [{'area_id': 0, 'networks': [{'ip': "137.78.5.0", 'wildmask': "0.0.0.255"},
                                                    {'ip': "61.128.1.0", 'wildmask': "0.0.0.255"},
                                                    {'ip': "1.1.1.1", 'wildmask': "0.0.0.0"}]}]}

c8kv2_ospf = {"processid": 1,
              "routerid": "2.2.2.2",
              "areas": [{'area_id': 0, 'networks': [{'ip': "61.128.1.0", 'wildmask': "0.0.0.255"},
                                                    {'ip': "202.100.1.0", 'wildmask': "0.0.0.255"},
                                                    {'ip': "2.2.2.2", 'wildmask': "0.0.0.0"}]}]}

# 汇总后数据
all_network_data = [{'ip': "196.21.5.211", 
                     'routername': 'C8kv1', 
                     'interfaces': c8kv1_ifs, 
                     'ospf': c8kv1_ospf,
                     'users': c8kv1_user
                     },
                    {'ip': "196.21.5.212", 
                     'routername': 'C8kv2', 
                     'interfaces': c8kv2_ifs, 
                     'ospf': c8kv2_ospf,
                     'users': c8kv2_user
                     }
                    ]

# 把之前的内容删除
session.query(Router).delete()

# 先添加LoginCredential
login_credential = LoginCredential(credential_name=login_credential['credential_name'], 
                                   username=login_credential['username'], 
                                   password=login_credential['password'])
session.add(login_credential)

# 先添加DeviceType
device_type = DeviceType(device_type=device_type['device_type'])
session.add(device_type)

# 添加Router
for device in all_network_data:
    # 添加Router
    router_device = Router(routername=device['routername'], ip=device['ip'])
    session.add(router_device)

    # 添加Interface
    for ifs in device['interfaces']:
        new_if = Interface(router=router_device, interface_name=ifs['ifname'], ip=ifs['ip'], mask=ifs['mask'])
        session.add(new_if)
    
    # 添加LoginCredential
    router_device.login_credential = login_credential
    # 添加DeviceType
    router_device.device_type = device_type
    
    # 添加OSPFProcess
    router_device_process = OSPFProcess(router=router_device,
                                        processid=device["ospf"]["processid"],
                                        routerid=device["ospf"]["routerid"])

    # 添加Area
    for device_area in device["ospf"]["areas"]:
        router_device_area = Area(ospf_process=router_device_process, area_id=device_area["area_id"])
        session.add(router_device_area)

        # 添加Area下的每一个OSPFNetwork
        for net in device_area["networks"]:
            new_net = OSPFNetwork(area=router_device_area, network=net['ip'], wildmask=net['wildmask'])
            session.add(new_net)
    
    # 添加User
    for user in device["users"]:
        new_user = User(router=router_device, username=user['username'], password=user['password'], priv=user['priv'])
        session.add(new_user)

session.commit()
