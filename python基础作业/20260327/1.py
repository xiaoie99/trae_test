import re

# 原始数据（多行字符串）
asa_conn = """TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO\n
TCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"""

# 存储结果的字典
conn_dict = {}

# 按行分割处理
for line in asa_conn.split('\n'):
    # 使用正则表达式提取信息
    # 匹配格式: 源IP:源端口 目的IP:目的端口 ... bytes 数字, flags 字母
    match = re.search(r'Student (\d+\.\d+\.\d+\.\d+):(\d+) Teacher (\d+\.\d+\.\d+\.\d+):(\d+).*bytes (\d+), flags (\w+)', line)
    
    if match:
        # 提取各组数据
        src_ip = match.group(1)
        src_port = match.group(2)
        dst_ip = match.group(3)
        dst_port = match.group(4)
        bytes_num = match.group(5)
        flags = match.group(6)
        
        # 键：(源IP, 源端口, 目的IP, 目的端口)
        key = (src_ip, src_port, dst_ip, dst_port)
        # 值：(bytes, flags)
        value = (bytes_num, flags)
        
        # 存入字典
        conn_dict[key] = value

# 打印字典
print("打印分析后的字典:")
print(conn_dict)
print("\n格式化打印输出:")
print("="*86 + "\n")

# 格式化打印输出
for key, value in conn_dict.items():
    src_ip, src_port, dst_ip, dst_port = key
    bytes_num, flags = value
    
    # 第一行：连接信息
    print("src       : {:<15} | src_port  : {:<6} | dst       : {:<15} | dst_port  : {:<6}".format(
        src_ip, src_port, dst_ip, dst_port))
    
    # 第二行：字节数和标志
    print("bytes     : {:<15} | flags     : {:<6}".format(bytes_num, flags))
    
    # 分隔线
    print("="*86)