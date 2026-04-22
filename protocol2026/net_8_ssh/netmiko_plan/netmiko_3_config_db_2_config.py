from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
from pathlib import Path
import os
from jinja2 import Template
from pprint import pprint
from netmiko_3_config_db_0_async_netmiko import netmiko_config_cred
import asyncio
import yaml
# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_dir = current_file.parent
sys.path.append(str(current_dir))

from netmiko_3_config_db_0_create_db import Router, Interface, OSPFProcess, Area, OSPFNetwork, db_filename
from netmiko_3_config_db_0_create_db import User, LoginCredential

engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()

# 设置模板目录
template_dir = f'{current_dir}{os.sep}config-template'
# 获取所有模板的文件
config_all_template_path = f'{template_dir}{os.sep}config-all.jinja2'

with open(config_all_template_path, 'r') as f:
    config_all_template = Template(f.read())

# 获取所有Router
routers = session.query(Router).all()

# 协程列表
coros = []

for router in routers:
    router_name = router.routername
    device_ip = router.ip
    login_credential = router.login_credential
    username = login_credential.username
    password = login_credential.password

    device_type = router.device_type.device_type

    router_dict = router.to_dict()
    # 把 router_dict 转成 YAML 字符串再打印，便于阅读
    print(yaml.safe_dump(router_dict, allow_unicode=True, sort_keys=False))
    config_all_config = config_all_template.render(router_dict=router_dict)
    config_all_config_str = [line.strip() for line in config_all_config.split('\n') if line.strip()]
    # print(config_all_config_str)
    coros.append(netmiko_config_cred(device_ip,
                                     username,
                                     password,
                                     config_all_config_str,
                                     device_type,
                                     verbose=True))


# 使用 asyncio.run + gather 并发执行并收集结果
async def _gather_all():
    return await asyncio.gather(*coros, return_exceptions=True)


result_list = asyncio.run(_gather_all())

# 打印任务结果
for r in result_list:
    print(r)
