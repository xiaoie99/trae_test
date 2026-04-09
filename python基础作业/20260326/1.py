import os
import re

route_n_result = os.popen("route -n").read()

# 这样写可以匹配多个网关
match = re.findall(r'^0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+).*UG', route_n_result, re.MULTILINE)

if match:
    for gateway in match:
        print(f"网关为: {gateway}")
else:
    print("未找到网关")