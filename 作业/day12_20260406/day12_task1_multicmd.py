import paramiko
import time
def qytang_multicmd(ip, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    """
    参数说明：
      cmd_list  : 要执行的命令列表，例如 ['terminal length 0', 'show version']
      enable    : enable 密码，若设备无需 enable 则保持默认空字符串
      wait_time : 每条命令发送后等待设备响应的秒数
      verbose   : True 则打印每条命令的返回结果，False 则静默执行
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=username, password=password,
                timeout=5, look_for_keys=False, allow_agent=False)
    chan = ssh.invoke_shell()
    time.sleep(1)
    chan.recv(65535)  # 清空欢迎信息
    # 如果需要 enable
    if enable:
        chan.send(b'enable\n')
        time.sleep(1)
        chan.send(enable.encode() + b'\n')
        time.sleep(1)
        chan.recv(65535)
    results = []
    for cmd in cmd_list:
        if verbose:
            print(f"\n--- {cmd} ---")
        chan.send(cmd.encode() + b'\n')
        time.sleep(wait_time)
        output = chan.recv(65535).decode()
        if verbose:
            print(output)
        results.append(output)
    ssh.close()
    return results
# 测试代码
if __name__ == "__main__":
    cmd_list = [
        'terminal length 0',
        'show version',
        'config ter',
        'router ospf 1',
        'network 10.0.0.0 0.0.0.255 area 0',
        'end',
    ]
    qytang_multicmd('10.10.1.200', 'admin', 'qwert@12345', cmd_list, wait_time=2, verbose=True)