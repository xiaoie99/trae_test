"""
网络设备接口配置管理脚本
使用类（Class）和组合（Composition）实现批量接口配置下发
"""
import sys
import os
# 导入第十二天的 qytang_multicmd 函数
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day12_20260406.day12_task1_multicmd import qytang_multicmd
class Interface:
    """接口配置类，只保存接口数据"""
    def __init__(self, name):
        self.name = name
        self.device = None           # 所属设备，默认未绑定
        self.ip_address = ''         # IP 地址，默认空字符串
        self.mask = ''               # 子网掩码，默认空字符串
        self.description = ''        # 接口描述，默认空字符串
        self.status = False          # True=no shutdown, False=shutdown，默认关闭
    def __str__(self):
        """格式化打印接口信息"""
        status_str = 'no shutdown' if self.status else 'shutdown'
        device_ip = self.device.ip if self.device else '未绑定设备'
        lines = [
            f"接口名称    : {self.name}",
            f"所属设备    : {device_ip}",
            f"IP 地址     : {self.ip_address} {self.mask}",
            f"描述        : {self.description}",
            f"状态        : {status_str}",
        ]
        return '\n'.join(lines)
class NetworkDevice:
    """网络设备类，保存设备登录信息及关联的接口"""
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.interfaces = []
    def add_interface(self, interface):
        """将接口加入本设备，并建立双向关联"""
        interface.device = self      # 把 interface 的 device 属性指向自己（self）
        self.interfaces.append(interface)  # 把 interface 追加到 self.interfaces 列表
    def apply(self):
        """将所有关联接口的配置一次性下发到设备"""
        if not self.interfaces:
            print(f"[*] {self.ip} 没有待下发的接口配置")
            return
        cmds = ['config ter']
        for iface in self.interfaces:
            cmds.append(f'interface {iface.name}')
            cmds.append(f'ip address {iface.ip_address} {iface.mask}')
            if iface.description:
                cmds.append(f'description {iface.description}')
            cmds.append('no shutdown' if iface.status else 'shutdown')
        cmds.append('end')
        iface_names = ', '.join(iface.name for iface in self.interfaces)
        print(f"[*] 正在 {self.ip} 上批量应用接口配置: {iface_names}")
        qytang_multicmd(self.ip, self.username, self.password, cmds, verbose=False)
        print(f"[*] {self.ip} 所有接口配置应用完成！")
    def __str__(self):
        """打印设备信息及下属接口列表"""
        lines = [
            f"设备 IP      : {self.ip}",
            f"用户名       : {self.username}",
            "接口列表     :",
        ]
        if not self.interfaces:
            lines.append("  （无）")
        else:
            for iface in self.interfaces:
                status_str = 'no shutdown' if iface.status else 'shutdown'
                lines.append(f"  - {iface.name}: {iface.ip_address} {iface.mask}, {status_str}")
        return '\n'.join(lines)
if __name__ == '__main__':
    # 1. 实例化设备对象（请填入实际的设备 IP、用户名、密码）
    r1 = NetworkDevice('10.10.1.200', 'admin', 'qwert@12345')
    # 2. 创建第一个接口并设置参数
    loop13 = Interface('Loopback13')
    loop13.ip_address = '13.13.13.13'
    loop13.mask = '255.255.255.255'
    loop13.description = 'Created_by_Python'
    loop13.status = True
    r1.add_interface(loop13)
    # 3. 创建第二个接口并设置参数
    gi2 = Interface('GigabitEthernet2')
    gi2.ip_address = '172.16.1.12'
    gi2.mask = '255.255.255.0'
    gi2.description = 'Created_by_Python'
    gi2.status = True
    r1.add_interface(gi2)
    # 4. 打印设备及下属所有接口
    print(r1)
    # 5. 一次 SSH 连接，批量下发所有接口配置
    r1.apply()