from netmiko import Netmiko
import yaml
import os
from jinja2 import Template
from pprint import pprint
import asyncio
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_dir = current_file.parent


async def netmiko_config_cred(host,
                              username,
                              password,
                              cmds_list,
                              device_type,
                              enable='Cisc0123',
                              verbose=False,
                              ssh_port=22
                              ):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'secret': enable,
                    'port': ssh_port
    }
    try:
        # 在线程池中运行同步的Netmiko操作
        def connect_and_send():
            net_connect = Netmiko(**device_info)
            try:
                # 使用 try/finally 确保连接异常时也能正常断开
                if verbose:
                    output = net_connect.send_config_set(cmds_list)
                    return output
                else:
                    net_connect.send_config_set(cmds_list)
                    return None
            finally:
                net_connect.disconnect()

        # 使用线程池运行同步函数
        return await asyncio.to_thread(connect_and_send)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


config_devices_info_dir = f'{current_dir}{os.sep}config-devices-info'
devices_config_file_name = 'devices_config.yaml'

config_template_dir = f'{current_dir}{os.sep}config-template'

# 协程列表
coros = []

# 读取设备配置文件
with open(
    f'{config_devices_info_dir}{os.sep}{devices_config_file_name}'
) as data_f:
    devices_config_data = yaml.safe_load(data_f.read())
    # 遍历设备配置文件
    for device in devices_config_data:
        configs = device.get('configs')
        device_ip = device.get('device_ip')
        device_type = device.get('device_type')
        username = device.get('username')
        password = device.get('password')
        total_cmd_list = []
        for config in configs:
            # 读取配置方向
            config_direction = config.get('config_direction')
            # 读取特定方向的配置模板文件
            template_file_name = f'{config_direction}.jinja2'
            with open(
                f'{config_template_dir}{os.sep}{template_file_name}'
            ) as template_f:
                # 读取配置模板文件
                template = Template(template_f.read())
                # 渲染产生配置命令
                config_str = template.render(config.get('config_data'))
                # 生成配置命令列表
                cmd_list = [
                    line.strip()
                    for line in config_str.split('\n')
                    if line.strip()
                ]
                total_cmd_list.extend(cmd_list)
        pprint(total_cmd_list)
        coros.append(netmiko_config_cred(device_ip,
                                         username,
                                         password,
                                         total_cmd_list,
                                         device_type,
                                         verbose=True
                                         ))


# 使用 asyncio.run + gather 并发执行并收集结果
async def _gather_all():
    return await asyncio.gather(*coros, return_exceptions=True)


result_list = asyncio.run(_gather_all())

# 打印任务结果
for r in result_list:
    print(r)
