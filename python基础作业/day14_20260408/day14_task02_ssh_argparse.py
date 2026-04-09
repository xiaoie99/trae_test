import argparse
import paramiko
def ssh_run(host, username, password, command):
    """通过 paramiko 执行 SSH 命令并返回结果"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=22, username=username, password=password, timeout=5,
                look_for_keys=False, allow_agent=False)
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()
    ssh.close()
    return result
def main():
    parser = argparse.ArgumentParser(description='网络设备 SSH 命令执行工具')
    # 添加四个参数：-i/--ip, -u/--username, -p/--password, -c/--cmd
    parser.add_argument('-i', '--ip', required=True, help='设备的 IP 地址')
    parser.add_argument('-u', '--username', required=True, help='登录用户名')
    parser.add_argument('-p', '--password', required=True, help='登录密码')
    parser.add_argument('-c', '--cmd', required=True, help='要执行的命令')
    args = parser.parse_args()
    # 调用 ssh_run 函数执行命令，并打印结果
    result = ssh_run(args.ip, args.username, args.password, args.cmd)
    print(result)
if __name__ == '__main__':
    main()