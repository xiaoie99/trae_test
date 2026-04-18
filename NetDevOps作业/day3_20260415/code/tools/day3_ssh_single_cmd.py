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
