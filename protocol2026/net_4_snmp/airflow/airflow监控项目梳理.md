# Airflow 监控项目梳理

## 1. 项目目标

这个项目做了两件事：

1. 通过 SNMPv3 周期性采集网络设备运行状态（CPU、内存、接口），写入 PostgreSQL。
2. 通过 Netmiko 周期性备份设备配置，发现变更后生成 diff，结合本地 AI 分析，邮件通知。

---

## 2. 项目整体架构

```
docker compose 启动的容器
====================================================================

基础设施层
├── postgres              Airflow 自己的元数据库
├── redis                 Celery Broker（消息队列）
└── qytpg                 业务 PostgreSQL（保存监控数据和配置备份）

初始化层（一次性任务，执行完就退出）
├── airflow-init          初始化 Airflow 数据库 + 创建管理员账号
└── airflow-create-tables 自动建业务表（router_monitor / routerconfig）

Airflow 服务层
├── airflow-webserver     Web UI（http://196.21.5.228:8088）
├── airflow-scheduler     调度 DAG
├── airflow-worker        执行 Celery 任务
└── airflow-triggerer     处理 deferrable task

====================================================================

启动顺序：
  postgres + redis 健康
    → airflow-init 完成
      → qytpg 健康
        → airflow-create-tables 建表完成
          → webserver / scheduler / worker / triggerer 启动
```

---

## 3. 两条核心业务链路

### 3.1 链路一：SNMP 监控写库（每 30 秒）

```
DAG: get_snmp_info_writedb_dag
│
├─ 入口文件: orm_2_write_db_dag.py
│    └─ PythonOperator 调用 get_info_writedb()
│
├─ 执行文件: orm_2_write_db.py
│    ├─ 调用 snmp_v3_3_get_all.py → snmpv3_get_all()
│    │    ├─ snmp_v3_1_get.py     → 获取单个 OID（主机名、CPU、内存）
│    │    └─ snmp_v3_2_getbulk.py → 批量获取接口名称、速率、流量
│    │
│    ├─ 组装数据字典（去掉 hostname 和 interface_list）
│    ├─ 添加 record_datetime（东八区时间）
│    ├─ 创建 RouterMonitor 对象
│    └─ session.add() + commit() 写入数据库
│
├─ 模型定义: orm_1_create_table.py
│    └─ RouterMonitor 类（对应 router_monitor 表）
│
└─ 写入目标: qytpg 数据库 → router_monitor 表
     ├─ device_ip          设备 IP
     ├─ cpu_usage_percent   CPU 使用率
     ├─ mem_usage_percent   内存使用率
     └─ record_datetime     记录时间
```

### 3.2 链路二：配置备份 + 差异检测 + AI 分析 + 邮件通知（每 1 分钟）

```
DAG: config_bak_and_diff_notification_dag
│
├─ 入口文件: config_diff_4_dag.py
│    └─ PythonOperator 调用 config_diff_and_notification()
│
├─ 核心文件: config_diff_3_get_md5_config.py
│    │
│    ├─ 第一步：采集配置
│    │    ├─ 调用 config_diff_0_netmiko_show.py
│    │    │    └─ Netmiko SSH 登录设备 → 执行 show run
│    │    ├─ 清洗配置（去掉头部无用信息）
│    │    └─ 计算当前配置的 MD5
│    │
│    ├─ 第二步：变更检测
│    │    ├─ 查询数据库中该设备最后一条 RouterConfig 记录
│    │    └─ 对比当前 MD5 与历史 MD5
│    │
│    ├─ 第三步：如果 MD5 不同（配置发生变更）
│    │    ├─ 生成 HTML Diff（config_diff_2_dff_conf.py，基于 difflib）
│    │    ├─ 调用本地 AI 分析变更（config_diff_0_ai.py）
│    │    │    └─ Ollama phi4 模型，用中文解释每个变更点
│    │    ├─ 使用 Jinja2 模板渲染完整 HTML 邮件
│    │    └─ 发送邮件通知（qyt_send_mail.py）
│    │
│    └─ 第四步：无论是否变化，都保存当前配置到数据库
│
├─ 模型定义: config_diff_1_create_table.py
│    └─ RouterConfig 类（对应 routerconfig 表）
│
└─ 写入目标: qytpg 数据库 → routerconfig 表
     ├─ device_ip     设备 IP
     ├─ config        完整配置内容
     ├─ md5           配置的 MD5 值
     └─ record_time   记录时间
```

---

## 4. 文件职责一览

### 4.1 SNMP 监控相关

| 文件 | 职责 |
| --- | --- |
| `orm_2_write_db_dag.py` | DAG 定义：`get_snmp_info_writedb_dag`，每 30 秒 |
| `orm_2_write_db.py` | 采集 SNMP 数据并写库 |
| `snmp_v3_3_get_all.py` | 聚合 CPU、内存、接口信息 |
| `snmp_v3_1_get.py` | SNMPv3 单 OID 获取 |
| `snmp_v3_2_getbulk.py` | SNMPv3 批量获取 |
| `orm_1_create_table.py` | `RouterMonitor` 表模型定义 |

### 4.2 配置备份与变更分析相关

| 文件 | 职责 |
| --- | --- |
| `config_diff_4_dag.py` | DAG 定义：`config_bak_and_diff_notification_dag`，每 1 分钟 |
| `config_diff_3_get_md5_config.py` | 核心逻辑：采集 → MD5 对比 → Diff → AI → 邮件 |
| `config_diff_0_netmiko_show.py` | Netmiko SSH 登录设备执行 show run |
| `config_diff_2_dff_conf.py` | 生成 HTML diff 片段（基于 difflib） |
| `config_diff_0_ai.py` | 调用 Ollama AI 解释配置变更 |
| `config_diff_1_create_table.py` | `RouterConfig` 表模型定义 |

### 4.3 公共模块

| 文件 | 职责 |
| --- | --- |
| `qyt_send_mail.py` | 邮件发送（支持 HTML 正文和附件） |
| `basic_info.py` | 邮件账号基础信息 |

---

## 5. 当前写死的配置

| 配置项 | 当前值 | 位置 |
| --- | --- | --- |
| 业务数据库地址 | `196.21.5.228` | orm_1_create_table.py 等多处 |
| Airflow Web 地址 | `http://196.21.5.228:8088` | docker-compose.yaml |
| SNMP 设备 IP | `196.21.5.211` | orm_2_write_db.py |
| Netmiko 设备 IP | `196.21.5.211` | config_diff_3_get_md5_config.py |
| 设备登录账号 | `admin / Cisc0123` | config_diff_3_get_md5_config.py |
| SNMP 认证信息 | `qytanguser / Cisc0123` | orm_2_write_db.py |
| AI 服务地址 | `http://196.21.5.228:11434/v1/` | config_diff_0_ai.py |
| 邮件账号 | `3348326959@qq.com` | qyt_send_mail.py / basic_info.py |

---

## 6. 快速启动

```bash
cd /Protocol2026/net_4_snmp/airflow

# 创建必要目录
mkdir -p ./dags ./logs ./plugins ./config

# 设置 AIRFLOW_UID
echo "AIRFLOW_UID=$(id -u)" > .env

# 启动（首次需要 --build）
docker compose up -d --build

# 查看状态
docker compose ps

# 查看建表任务是否成功
docker compose logs airflow-create-tables
```

登录地址：`http://196.21.5.228:8088`
默认账号：`airflow / airflow`
