### VSCODE几个关键设置
```shell
"python.terminal.executeInFileDir": true, # 在文件目录执行
"terminal.integrated.env.windows": {
  "PYTHONPATH": "${workspaceFolder}"  # 把根目录加载到PATHPATH
},
"python.envFile": "${workspaceFolder}/.env",  # 加载.env
"python.analysis.extraPaths": ["${workspaceFolder}"]
```