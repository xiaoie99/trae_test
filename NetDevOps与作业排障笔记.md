# NetDevOps 与作业排障笔记（已解决问题汇总）

> 本文整理自课程实践与对话中**已确认**的做法与结论，便于新对话或复习时快速对齐，而不必重复翻全部聊天记录。  
> 路径以本仓库 **`/python_basic`** 为准；若你机器上路径不同，请自行替换。

---

## 1. Docker 与 Compose

### 1.1 安装与启用（CentOS / RHEL 系示例）

来自 Day5 作业 README，用于安装 Docker CE 并开机自启 Docker **服务**（注意：这是「Docker 引擎」自启，与下面「容器是否自启」是两件事）：

```bash
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
systemctl start docker
systemctl enable docker
```

验证：

```bash
docker --version
docker compose version
```

### 1.2 `docker compose` 与 `docker-compose`（已确认结论）

- **推荐**：使用 **Compose v2 插件**：命令为 **`docker compose`**（中间有空格）。
- **不推荐**：用 `pip install docker-compose` 老独立二进制；在 **Python 3.12** 等环境下常装不上或易踩坑。
- 若 `docker compose version` 正常，**不必**再单独安装旧版 `docker-compose`。

### 1.3 怎么「运行和拉起」作业里的 Influx + Grafana

本质是：**先 `cd` 到存放 Compose 文件的目录**，再指定 **`-f` 文件** 执行 **`up -d`**。

**Day5**（仓库内文件：`NetDevOps作业/day5_20260417/influxdb_grafana.yaml`）：

```bash
cd /python_basic/NetDevOps作业/day5_20260417
docker compose -f influxdb_grafana.yaml up -d
docker ps
```

**Day6**（仓库内文件：`NetDevOps作业/day6_20260420/code/docker-compose.yaml`）：

```bash
cd /python_basic/NetDevOps作业/day6_20260420/code
docker compose -f docker-compose.yaml up -d
docker ps
```

预期常见容器名（与 Compose 中 `services` 名一致）：**`qyt-influx`**、**`qyt-grafana`**。

若 `docker compose` 报错，可先查引擎：

```bash
systemctl status docker
systemctl restart docker
```

### 1.4 怎么停止、怎么「重建」

停止并删除该 Compose 项目下的容器（网络等按 Compose 定义处理）：

```bash
# Day5 示例（目录与 -f 须与启动时一致）
cd /python_basic/NetDevOps作业/day5_20260417
docker compose -f influxdb_grafana.yaml down

# Day6 示例
cd /python_basic/NetDevOps作业/day6_20260420/code
docker compose -f docker-compose.yaml down
```

端口冲突或环境异常时，常用「先 down 再 up」：

```bash
ss -lntp | grep -E '(:3000|:8086)'
docker compose -f <你的yaml> down
docker compose -f <你的yaml> up -d
```

查看日志：

```bash
docker compose -f <你的yaml> ps
docker compose -f <你的yaml> logs --tail=100
```

### 1.5 系统重启后「容器会不会自己起来」

当前作业用的 Compose 里，服务配置了 **`restart: always`**（见 `influxdb_grafana.yaml` 与 `docker-compose.yaml`）。含义是：

- 只要 **Docker 引擎** 在跑，容器异常退出后会重启；
- **主机重启**后，若 Docker 服务也随系统启动，这些容器一般会再次被拉起。

若你希望**重启机器后不要自动拉起这组容器**，可选用其一（按你是否还要保留其他 Docker 用途选择）：

1. **改 Compose 文件**（需重新 `up` 才生效）：把 `restart: always` 改为 `restart: "no"` 或 `unless-stopped`（行为略有区别，按需查官方文档）。
2. **平时不用就 down**：关机前或维护后执行 `docker compose ... down`，则没有运行中的容器；但若未改 `restart` 且有人再次 `up -d`，以后重启仍可能自动起。
3. **对已运行的容器改策略**（不改 yaml 时）：`docker update --restart=no <容器名或ID>`（具体是否受 Compose 再次 reconcile 影响以你环境为准，**最稳仍是改 yaml + down/up**）。

**注意**：`systemctl disable docker` 会关掉整个 Docker 服务，一般**不建议**作为作业场景下的常规做法。

### 1.6 如何查看当前有哪些容器在跑、「运行目录」是什么

**查看运行中容器**：

```bash
docker ps
docker ps -a
```

**查看 Compose 项目**（v2 常用）：

```bash
docker compose ls
```

**「运行目录」在实践里通常指两件事**（对话里已对齐过语义）：

1. **你执行 `docker compose up` 时所在的当前工作目录（cwd）**  
   Compose 默认用该目录作为 **project 的上下文**，且相对路径（如 volume 的 `./data`）相对这里解析。因此 **启动时务必 `cd` 到 README 写明的目录**，与作业一致。

2. **Compose 文件来自哪里**  
   可用下面命令看容器标签里的配置路径（需把 `<容器名>` 换成 `docker ps` 里看到的，如 `qyt-grafana`）：

```bash
docker inspect <容器名> --format '{{json .Config.Labels}}' | tr ',' '\n' | grep -i compose
```

常见标签：`com.docker.compose.project.config_files`、`com.docker.compose.project.working_dir`（若存在，可对应到当时启动的目录/compose 路径）。

---

## 2. InfluxDB 与 Grafana 配置（已踩坑并解决）

### 2.1 Grafana 里 Influx 数据源的 URL（重要）

- **在 Grafana 容器内部**访问 InfluxDB 时，应使用 **服务名**：**`http://qyt-influx:8086`**（与 Compose 里 `services` 名称一致），**不要**填 `http://127.0.0.1:8086`（那指向 Grafana 容器自己，除非你做 host 网络等特殊映射）。
- Day5 README 里写过：若「按服务名不通」再考虑本机其它访问方式；在标准 **bridge + 同 compose 网络** 下，**`qyt-influx` 才是正确习惯**。

### 2.2 数据源账号与库名（与作业 README 一致）

| 项 | 值 |
| --- | --- |
| Type | InfluxDB |
| Query Language（Day6） | InfluxQL（见 `grafana.md`） |
| URL | `http://qyt-influx:8086` |
| Database | `qytdb` |
| User | `qytdbuser` |
| Password | `Cisc0123` |

Compose 环境变量里会创建库 **`qytdb`** 与用户；若曾手动删库或数据损坏，可 **`docker compose down` 后 `up -d`** 让初始化逻辑重新跑（**注意：可能清空容器内数据**，生产环境勿照搬）。

### 2.3 Grafana 面板与查询（Day5 / Day6）

- **Day5**（CPU/内存）：README 中已给出两条 `SELECT mean("cpu_usage")` / `mean("mem_usage")` 的 InfluxQL 示例，`FROM "router_monitor"`，`GROUP BY` 带 `device_ip`。
- **Day6**（接口速率）：详见同目录 **`grafana.md`**（TX/RX 使用 `non_negative_derivative`、`interface_monitor`、`bits/sec` 单位、Alias 等）。

**已确认过的体验优化**：

- Grafana 图表面板里 **Tooltip** 建议设为 **「All」** 一类选项，便于同一时刻多条曲线一起显示（多设备或多序列时）。

### 2.4 宿主机访问端口

- **Grafana Web**：`http://<服务器IP>:3000`（默认 `admin/admin`，首次登录会要求改密）。
- **InfluxDB HTTP API**：宿主机上常用 **`http://127.0.0.1:8086`**（因 compose 映射了 `8086:8086`）；这与 **Grafana 容器内填 `qyt-influx:8086`** 不矛盾。

---

## 3. Python 采集脚本与 crond（已对齐做法）

### 3.1 虚拟环境与解释器路径

crontab 里**不要**写裸 `python3`，应写 **venv 里解释器的绝对路径**，避免环境变量与包不一致，例如：

```text
/python_basic/.venv/bin/python
```

### 3.2 每分钟：`*/1` 与 `* * * * *`

在 crontab 的五段式里，**每分钟执行**写 `*/1 * * * *` 与 `* * * * *` **效果相同**（都是每分钟触发）。作业里两种写法都曾出现，任选其一即可，注意 **crond 需 root 或对应用户权限** 与日志重定向。

### 3.3 Day5 / Day6 日志与示例行

- Day5 采集日志示例：`/tmp/day5_influx.log`
- Day6：`/tmp/day6_sqlite.log`、`/tmp/day6_influx.log`

修改 `/etc/crontab` 或用户 crontab 后：

```bash
systemctl restart crond.service
tail -f /tmp/day5_influx.log
```

### 3.4 SNMP 与设备参数（你已确认沿用）

作业脚本中常见默认：

- **`10.10.1.200` / `qytangro`**
- **`10.10.1.201` / `qytangro`**

若采集超时，优先查：IP、community、设备 SNMP 配置、ACL、路由连通性。

### 3.5 Python 依赖（已遇到问题并解决）

- 报错 **`ModuleNotFoundError: influxdb`**：在使用的 venv 中执行  
  `/python_basic/.venv/bin/pip install influxdb`
- Day6 常用组合（见 Day6 README）：  
  `sqlalchemy numpy bokeh influxdb pysnmp`

### 3.6 SQLAlchemy 警告（已按课件/新版本习惯处理）

- 若出现 **`MovedIn20Warning`** 一类与 `declarative_base` 相关的提示，**从 `sqlalchemy.orm` 引入 `declarative_base`**（而不是旧式 `sqlalchemy.ext.declarative`），与当前 SQLAlchemy 2.x 文档一致。作业 `day6_1_create_db.py` 已按此方向对齐。

### 3.7 Day6 包路径与工具脚本

- `day6_2`、`day6_4` 等通过 **`sys.path.insert`** 把 **`day6_20260420` 的上一级**（即包含 **`code` 包**的那层）加入路径，从而 `from code.tools...` 可导入。
- **`day6_snmp_get_all`** 聚合 **`day6_snmp_getbulk`** 的 GETBULK 结果；单独跑工具脚本时，若遇 import 错误，需从 README 指定目录运行或保持与同作业一致的 path 处理。

---

## 4. 其它零散但已结论化的问题

### 4.1 Git 与仓库体积

- 曾将 **`/protocol2026/`** 加入 **`.gitignore`**，并对已跟踪目录执行 **`git rm -r --cached`**，避免大课件目录进入版本库。若你本地仍需课件，保留在工作区即可，不必提交。

### 4.2 Cursor + DeepSeek（非 Docker，属编辑器配置）

- 使用 **OpenAI API Key** 字段 + **Override base URL** 指向 DeepSeek 的 OpenAI 兼容地址（如 `https://api.deepseek.com/v1`），自定义模型名 **`deepseek-chat`**。
- 若出现与 **`image_url` / 多模态** 相关的 **Provider Error**，多为**当前会话混入了图片上下文**；**新开纯文本对话**再调用可避免。

### 4.3 作业文档粘贴

- 部分环境粘贴到 Word/实验报告时，曾处理过 **多余空行**；与代码正确性无关，按需保留可读版式即可。

---

## 5. 新对话里如何让别人「接着这份笔记干活」

可复制下面模板，把路径改成你的机器上的实际路径即可：

```text
请先阅读 /python_basic/NetDevOps与作业排障笔记.md 与（如需）SUPER_INDEX.md。
当前任务：（写你的作业或故障现象）
已做过：（写你已执行的命令，如 compose up、crontab 行）
不要重复通读 protocol2026 全目录，除非索引指向必须细读的文件。
```

---

*若后续你又确认了新的结论（例如换了 Influx 2.x、Grafana 大版本），建议在本文件末尾按日期追加一节「变更记录」，避免旧结论误导以后的自己。*
