from netmiko import Netmiko
import asyncio

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
                # 使用 try/finally 确保异常时也能正常断开连接
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