# NetDevOps 第五天作业

## 1) 安装 Docker / Docker Compose

```bash
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
systemctl start docker
systemctl enable docker
```

说明:
- 推荐使用 `docker compose`（Compose v2 插件）
- 如果你系统里只有 `docker compose`，可以不安装 `docker-compose`

## 2) 启动 InfluxDB + Grafana

```bash
cd /python_basic/NetDevOps作业/day5_20260417
docker compose -f influxdb_grafana.yaml up -d
docker ps
```

预期有两个容器运行:
- `qyt-influx`
- `qyt-grafana`

## 3) 测试采集并写入 InfluxDB

当前脚本默认设备参数如下（你已确认不变，可直接使用）:
- `10.10.1.200` / `qytangro`
- `10.10.1.201` / `qytangro`

```bash
/python_basic/.venv/bin/python /python_basic/NetDevOps作业/day5_20260417/day5_1_influxdb_monitor.py
```

## 4) Crond 调度

编辑 `/etc/crontab` 增加:

```cron
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

*/1 * * * * root /python_basic/.venv/bin/python /python_basic/NetDevOps作业/day5_20260417/day5_1_influxdb_monitor.py >> /tmp/day5_influx.log 2>&1
```

重启 crond:

```bash
systemctl restart crond.service
```

查看日志:

```bash
tail -f /tmp/day5_influx.log
```

## 5) Grafana 展示 CPU / 内存

1. 访问 `http://<你的服务器IP>:3000`（默认账号密码: `admin/admin`）
2. 添加 Data Source:
   - Type: InfluxDB
   - URL: `http://qyt-influx:8086`（若不通可改 `http://127.0.0.1:8086`）
   - Database: `qytdb`
   - User: `qytdbuser`
   - Password: `Cisc0123`
3. 新建 Dashboard 两个 Time series 面板:
   - CPU 利用率查询:
     - `SELECT mean("cpu_usage") FROM "router_monitor" WHERE $timeFilter GROUP BY time($__interval), "device_ip" fill(null)`
   - 内存利用率查询:
     - `SELECT mean("mem_usage") FROM "router_monitor" WHERE $timeFilter GROUP BY time($__interval), "device_ip" fill(null)`

## 6) 可选: 导入课程 Dashboard 模板

课程模板文件:

`/python_basic/protocol2026/net_4_snmp/practice_lab/lab2/QYT-influxDB-2022.json`

Grafana -> Create -> Import -> 上传该 JSON。

## 7) 常见故障排查（演示兜底）

1. `docker compose` 不可用

```bash
docker compose version
docker --version
```

- 若 `docker compose` 无输出或报错，先确认 Docker 服务状态:

```bash
systemctl status docker
systemctl restart docker
```

2. 端口冲突（3000/8086 被占用）

```bash
ss -lntp | grep -E '(:3000|:8086)'
docker compose -f influxdb_grafana.yaml down
docker compose -f influxdb_grafana.yaml up -d
```

3. 容器已启动但页面/写库异常

```bash
docker compose -f influxdb_grafana.yaml ps
docker compose -f influxdb_grafana.yaml logs --tail=100
tail -n 50 /tmp/day5_influx.log
```

- 若采集脚本报 SNMP 超时，优先检查路由器 IP、community、ACL 与连通性。
