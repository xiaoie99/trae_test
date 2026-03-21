import os
import shutil

# 第一步：创建backup目录
backup_dir = "backup"

# 如果目录已存在，先删除
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)

# 创建backup目录
os.makedirs(backup_dir)

# 配置文件内容
files = {
    'R1_config.txt': 'hostname R1\ninterface GigabitEthernet0/0\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R2_config.txt': 'hostname R2\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R3_config.txt': 'hostname R3\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'SW1_config.txt': 'hostname SW1\ninterface Vlan1\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
}

# 写入文件
for filename, content in files.items():
    filepath = os.path.join(backup_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)

print("配置文件已创建到 backup/ 目录")

# 第二步：遍历目录，找出含有shutdown（排除no shutdown）的配置文件
shutdown_files = []

# 获取backup目录中的所有文件
all_files = os.listdir(backup_dir)

# 检查每个文件
for filename in all_files:
    filepath = os.path.join(backup_dir, filename)
    
    # 只处理文件，忽略子目录
    if os.path.isfile(filepath):
        # 打开文件并读取内容
        with open(filepath, 'r') as f:
            content = f.read()
        
        # 按行分割内容
        lines = content.split('\n')
        
        # 检查每一行是否包含"shutdown"但不包含"no shutdown"
        found_shutdown = False
        for line in lines:
            if 'shutdown' in line and 'no shutdown' not in line:
                found_shutdown = True
                break  # 找到一次就跳出
        
        # 如果找到了shutdown，添加到列表
        if found_shutdown:
            shutdown_files.append(filename)

# 打印结果
print("\n发现包含 shutdown 接口的设备配置文件:")
for filename in shutdown_files:
    print(filename)

# 第三步：删除backup目录及其所有文件
shutil.rmtree(backup_dir)
print("\nbackup/ 目录已清理")