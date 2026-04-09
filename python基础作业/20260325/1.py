import os
import re

result = os.popen("ifconfig ens33").read()

# 第一步：用正则表达式提取IP、掩码、广播地址、MAC
# 提取IP地址
ip_pattern = r'inet\s+(\d+\.\d+\.\d+\.\d+)'
ip_match = re.search(ip_pattern, result)
ip = ip_match.group(1)

# 提取掩码
netmask_pattern = r'netmask\s+(\d+\.\d+\.\d+\.\d+)'
netmask_match = re.search(netmask_pattern, result)
netmask = netmask_match.group(1)

# 提取广播地址
broadcast_pattern = r'broadcast\s+(\d+\.\d+\.\d+\.\d+)'
broadcast_match = re.search(broadcast_pattern, result)
broadcast = broadcast_match.group(1)

# 提取MAC地址
mac_pattern = r'ether\s+([0-9a-fA-F:]{17})'
mac_match = re.search(mac_pattern, result)
mac = mac_match.group(1)

# 使用format()对齐打印
print("{:<12}: {}".format("IP", ip))
print("{:<12}: {}".format("Netmask", netmask))
print("{:<12}: {}".format("Broadcast", broadcast))
print("{:<12}: {}".format("MAC", mac))

# 第二步：根据IP地址的前三段拼接网关地址（已知网关为关 x.x.x.254）
ip_parts = ip.split('.')
gateway = ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + ".254"

print("\n已知网关为: " + gateway)

# 用os.popen执行ping测试
ping_result = os.popen("ping -c 2 -W 1 " + gateway).read()

# 判断是否ping通
# 只要不是0 received就算通
if "0 received" not in ping_result:
    print("Ping " + gateway + " ... reachable")
else:
    print("Ping " + gateway + " ... unreachable")
