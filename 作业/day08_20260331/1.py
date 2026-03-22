import os
import time
print("开始检测 TCP/80 端口状态...")
while True:
    # 获取所有端口信息
    result = os.popen('ss -tulnp').read()
    # 默认假设端口未监听
    port_listening = False
    # 逐行检查
    for line in result.split('\n'):
        # 检查是否同时包含 tcp 和 :80
        if 'tcp' in line and ':80 ' in line:  # 注意:80后面有个空格，避免匹配:8080
            port_listening = True
            break
    if port_listening:
        print("[!] 告警: TCP/80 已开放！请检查是否为授权服务。")
        break  # 退出循环
    else:
        print("[*] 检测中... TCP/80 未监听")
    # 等待1秒
    time.sleep(1)