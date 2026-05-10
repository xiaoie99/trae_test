import requests
import base64
import os
import sys
from flask import Flask, request
import subprocess
app = Flask(__name__)
if sys.platform == 'linux':
    server_ip = '10.10.1.205'
elif sys.platform == 'win32':
    server_ip = '10.10.1.205'
else:
    server_ip = '127.0.0.1'
server_port = '8080'
base_url = 'http://' + server_ip + ':' + server_port + '/'
exec_cmd_url = base_url + 'cmd'
upload_url = base_url + 'upload'
download_url = base_url + 'download'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_FILES_DIR = os.path.join(SCRIPT_DIR, 'server_files')
def system_cmd(cmd_command):
    result = subprocess.run(cmd_command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr
@app.route('/cmd', methods=['POST'])
def cmd():
    client_post_data = request.json
    if client_post_data:
        try:
            cmd_command = client_post_data.get('cmd')
        except AttributeError:
            return {'error': base64.b64encode('json format error'.encode()).decode()}
        if cmd_command:
            code, out, err = system_cmd(cmd_command)
            if code != 0:
                err_msg = err.strip() if err.strip() else out.strip()
                if not err_msg:
                    err_msg = 'command failed'
                return {'error': base64.b64encode(err_msg.encode()).decode()}
            if err.strip():
                return {'error': base64.b64encode(err.strip().encode()).decode()}
            return {'cmd': cmd_command, 'cmd_result': base64.b64encode(out.encode()).decode()}
        else:
            return {'error': base64.b64encode('no cmd in json'.encode()).decode()}
    else:
        return {'error': base64.b64encode('no json data'.encode()).decode()}
@app.route('/upload', methods=['POST'])
def upload():
    client_post_data = request.json
    if client_post_data:
        try:
            upload_filename = client_post_data.get('upload_filename')
            file_bit = client_post_data.get('file_bit')
        except AttributeError:
            return {'error': base64.b64encode('json format error'.encode()).decode()}
        if upload_filename and file_bit:
            os.makedirs(SERVER_FILES_DIR, exist_ok=True)
            file_bytes = base64.b64decode(file_bit.encode())
            save_path = os.path.join(SERVER_FILES_DIR, upload_filename)
            with open(save_path, 'wb') as f:
                f.write(file_bytes)
            return {'message': 'Upload Success!', 'upload_file': upload_filename}
        else:
            return {'error': 'need upload_filename and file_bit'}
    else:
        return {'error': 'no json data'}
@app.route('/download', methods=['POST'])
def download():
    client_post_data = request.json
    if client_post_data:
        try:
            download_filename = client_post_data.get('download_filename')
        except AttributeError:
            return {'error': base64.b64encode('json format error'.encode()).decode()}
        if download_filename:
            save_path = os.path.join(SERVER_FILES_DIR, download_filename)
            if os.path.isfile(save_path):
                with open(save_path, 'rb') as f:
                    file_data = f.read()
                return {'download_filename': download_filename, 'file_bit': base64.b64encode(file_data).decode()}
            else:
                return {'error': 'download file not exist'}
        else:
            return {'error': 'need download_filename'}
    else:
        return {'error': 'no json data'}
def json_rpc_client_exec_cmd(exec_cmd):
    response = requests.post(exec_cmd_url, json=exec_cmd)
    data = response.json()
    if 'error' in data:
        return base64.b64decode(data['error']).decode()
    return base64.b64decode(data['cmd_result']).decode()
def json_rpc_client_upload(upload_filepath):
    basename = os.path.basename(upload_filepath)
    with open(upload_filepath, 'rb') as f:
        file_bit = base64.b64encode(f.read()).decode()
    payload = {'upload_filename': basename, 'file_bit': file_bit}
    response = requests.post(upload_url, json=payload)
    return response.json()
def json_rpc_client_download(download_filename):
    payload = {'download_filename': download_filename}
    response = requests.post(download_url, json=payload)
    data = response.json()
    if 'error' in data:
        print(data['error'])
        return
    file_bytes = base64.b64decode(data['file_bit'].encode())
    with open(download_filename, 'wb') as f:
        f.write(file_bytes)
    print(download_filename + '下载成功!')
if __name__ == "__main__":
    # 1. 执行正确命令，应该返回正常结果
    exec_cmd = {'cmd': 'ifconfig'}
    print(json_rpc_client_exec_cmd(exec_cmd))
    # 2. 执行错误命令，应该返回错误输出
    exec_cmd = {'cmd': 'pwd1'}
    print(json_rpc_client_exec_cmd(exec_cmd))
    # 3. JSON 键名写错，应该返回 no cmd in json
    exec_cmd = {'cmd1': 'pwd'}
    print(json_rpc_client_exec_cmd(exec_cmd))
    # 4. 上传存在的文件，应该提示上传成功
    print(json_rpc_client_upload('logo.jpg'))
    # 5. 下载存在的文件，应该提示下载成功
    json_rpc_client_download('logo.jpg')
    # 6. 下载不存在的文件，应该提示文件不存在
    json_rpc_client_download('logo1.jpg')
