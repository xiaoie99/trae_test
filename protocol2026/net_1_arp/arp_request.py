#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/
from scapy.all import ARP, sr1


def arp_request(ip_address):
    try:  # 发送ARP请求并等待响应
        result_raw = sr1(ARP(pdst=ip_address),
                         timeout=1,
                         verbose=False
                         )
        return ip_address, result_raw.getlayer(ARP).fields.get('hwsrc')

    except AttributeError:
        return ip_address, None


if __name__ == "__main__":
    # Windows Linux均可使用
    arp_result = arp_request('196.21.5.1')
    print("IP地址:", arp_result[0], "MAC地址:", arp_result[1])
