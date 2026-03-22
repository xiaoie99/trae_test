import sys
import os
# 添加上级目录到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 导入重命名后的模块
from day08_20260331.day08_task02_ping_gateway import ping_check
from day09_20260401.day09_task01_ssh_gateway import ssh_run
def collect_interface_info(device_list):
    print("开始采集设备接口信息...")
    print("=" * 50)
    for ip, username, password in device_list:
        # 先ping检测
        print(f"正在检查设备: {ip}")
        reachable, rtt = ping_check(ip)
        if reachable:
            print(f"[*] {ip} 可达，正在采集...")
            # SSH连接并执行命令
            output = ssh_run(ip, username, password, "show ip interface brief")
            # 打印接口信息
            print(f"---------- {ip} 接口信息 ----------")
            # 检查输出是否是错误信息
            if output.startswith("认证失败") or output.startswith("SSH连接错误") or output.startswith("连接失败"):
                print(f"采集失败: {output}")
            else:
                print(output.strip())
            print()  # 空行分隔
        else:
            print(f"[x] {ip} 不可达，跳过，不采集。")
            print()
    print("采集完成！")
if __name__ == "__main__":
    devices = [
        ("192.168.0.206", "admin", "qwert@12345"),
        ("10.10.1.200", "admin", "qwert@12345"),
        ("192.168.0.205", "admin", "qwert@12345"),
    ]
    # 收集接口信息
    collect_interface_info(devices)
