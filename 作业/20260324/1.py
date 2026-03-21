import re

mac_table = '166    54a2.74f7.0326    DYNAMIC     Gi1/0/11'

match = re.match(r'(\d+)\s+([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+(\w+)\s+(\S+)', mac_table)

vlan = match.group(1)
mac = match.group(2)
mac_type = match.group(3)
port = match.group(4)

print("VLAN  : {}".format(vlan))
print("MAC   : {}".format(mac))
print("Type  : {}".format(mac_type))
print("Port  : {}".format(port))