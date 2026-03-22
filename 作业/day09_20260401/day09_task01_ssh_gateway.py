import re
import paramiko

def ssh_run(host, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password,
                   look_for_keys=False, allow_agent=False)
    stdin, stdout, stderr = client.exec_command(command)
    result = stdout.read().decode()
    client.close()
    return result

if __name__ == "__main__":
    # 执行命令
    output = ssh_run("10.10.1.205", "root", "qwert@12345", "route -n")
    # 提取所有默认网关
    for line in output.split('\n'):
        match = re.match(r'0\.0\.0\.0\s+([0-9.]+)\s+0\.0\.0\.0\s+.*?UG', line)
        if match:
            print(f"默认网关: {match.group(1)}")
