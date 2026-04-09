"""
现在有一个接口名字符串:

interface = "GigabitEthernet0/0/1"
通过切片的方式，分别提取出接口类型和接口编号，并打印:

接口类型: GigabitEthernet
接口编号: 0/0/1
提示: 先数一下 "GigabitEthernet" 有几个字符。
"""
interface = "GigabitEthernet0/0/1"

interface_type = interface[:15]
interface_number = interface[15:]
print(f"接口类型: {interface_type}")
print(f"接口编号: {interface_number}")
