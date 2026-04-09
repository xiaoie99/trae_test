import re

conn = 'TCP server  172.16.1.101:443 localserver  172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

match = re.match(r'(\w+)\s+\S+\s+([\d.]+):(\d+)\s+\S+\s+([\d.]+):(\d+)', conn)

protocol = match.group(1)
server_ip = match.group(2)
server_port = match.group(3)
client_ip = match.group(4)
client_port = match.group(5)

print("Protocol    : {}".format(protocol))
print("Server IP   : {}".format(server_ip))
print("Server Port : {}".format(server_port))
print("Client IP   : {}".format(client_ip))
print("Client Port : {}".format(client_port))