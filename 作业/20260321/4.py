"""
创建一个随机产生IP地址的代码
导入random模块，随机产生网络IPv4地址。
"""
import random

ip1=random.randint(0, 255)
ip2=random.randint(0, 255)
ip3=random.randint(0, 255)
ip4=random.randint(0, 255)

print(str(ip1) + "." + str(ip2) + "." + str(ip3) + "." + str(ip4))
