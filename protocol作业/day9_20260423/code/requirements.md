# Day 9 配置备份系统 - 作业要求

## 代码修改原则
1. 尽量不要修改老师给出的代码，除非遇到以下必须改的情况：
   (a) 题目明确要求学生自行完成的部分（如 ★ 标记处）
   (b) 某些路径如果不修改就无法正常运行

## 格式要求
- 生成的代码中不要有空行（避免粘贴给老师看时格式错乱）

## 任务说明
- 完成之后需要明确告知用户哪些部分需要用户自己操作

## 代码目录结构
```
day9_20260423/code/
├── __init__.py
├── day9_1_model.py              # 数据库模型（老师提供，未修改）
├── day9_2_init_db.py            # 创建数据表（老师提供，未修改）
├── day9_3_seed_devices.py       # 初始化设备清单（老师提供，未修改）
├── day9_4_config_diff_backup.py # 主程序（补齐了 ★ 标注的学生作业部分）
├── requirements.md              # 本说明文档
└── tools/
    ├── __init__.py
    ├── diff_config.py            # 配置差异比较工具（老师提供，未修改）
    ├── smtp_send_mail_attachment.py # 邮件发送工具（老师提供，未修改）
    └── ssh_client_netmiko.py     # Netmiko 采集工具（老师提供，未修改）
```

## 执行顺序
1. `python day9_2_init_db.py` - 建表
2. `python day9_3_seed_devices.py` - 初始化设备（需先修改为真实设备信息）
3. `python day9_4_config_diff_backup.py` - 执行采集、比对、告警、备份

## 需要用户自行操作的部分
1. 修改 `day9_3_seed_devices.py` 中 `TEST_DEVICES` 的设备 IP、用户名、密码、enable 密码
2. （可选）配置 SMTP 环境变量以启用邮件告警
3. （可选）配置 cron 定时调度