import sys
import os
import hashlib
import time
import re
# 添加上级目录到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 导入重命名后的模块
from day09_20260401.day09_task01_ssh_gateway import ssh_run
# 函数一：获取设备配置
def get_device_config(ip, username, password):
    """
    SSH登录思科路由器执行show running-config，
    截取hostname到end之间的有效配置部分，返回配置字符串
    """
    # 执行show running-config命令
    output = ssh_run(ip, username, password, "show running-config")
    # 检查是否有错误
    if output.startswith("认证失败") or output.startswith("SSH连接错误") or output.startswith("连接失败"):
        return None
    # 使用正则提取hostname到end之间的内容，贪婪匹配到最后一个end
    match = re.search(r'(hostname[\s\S]+end)', output)
    if match:
        return match.group(1)
    else:
        return None
# 函数二：每5秒监控一次配置变化
def monitor_config_change(ip, username, password):
    """
    每5秒获取设备配置，计算MD5值，检测配置是否变化
    """
    last_md5 = None
    while True:
        # 获取设备配置
        config = get_device_config(ip, username, password)
        if config is None:
            print(f"[!] 告警: 获取配置失败，请检查连接")
            break
        # 计算MD5值
        m = hashlib.md5()
        m.update(config.encode())
        current_md5 = m.hexdigest()
        # 判断是否第一次获取
        if last_md5 is None:
            print(f"[*] 当前配置 MD5: {current_md5}")
            last_md5 = current_md5
        else:
            # 比较MD5值
            if current_md5 == last_md5:
                print(f"[*] 当前配置 MD5: {current_md5}")
            else:
                print(f"[*] 当前配置 MD5: {last_md5}")
                print(f"[!] 告警: 配置已改变！新 MD5: {current_md5}")
                break
        # 等待5秒
        time.sleep(5)
if __name__ == "__main__":
    device_ip = "10.10.1.200"
    username = "admin"
    password = "qwert@12345"
    # 开始监控配置变化
    monitor_config_change(device_ip, username, password)
