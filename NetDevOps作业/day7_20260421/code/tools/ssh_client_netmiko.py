#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from netmiko import Netmiko
def netmiko_config_cred(host,
                        username,
                        password,
                        cmds_list,
                        device_type='cisco_ios',
                        verbose=False,
                        ssh_port=22):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'session_log': 'session_' + host + '.log',
                    'port': ssh_port
    }
    try:
        net_connect = Netmiko(**device_info)
        if verbose:
            output = net_connect.send_config_set(cmds_list)
            return output
        else:
            net_connect.send_config_set(cmds_list)
        net_connect.disconnect()
    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return
