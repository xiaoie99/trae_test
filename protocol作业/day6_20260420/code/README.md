# NetDevOps 第六天作业

## 目录

- `day6_1_create_db.py`：创建 SQLite 表
- `day6_2_write_sqlite.py`：SNMP 采集接口字节并写入 SQLite
- `day6_3_show_sqlite.py`：读取 SQLite，Numpy 计算 kbps，Bokeh 出图
- `day6_4_write_influxdb.py`：SNMP 采集接口字节并写入 InfluxDB
- `tools/`：SNMP 与 Bokeh 工具函数

## 依赖

```bash
/python_basic/.venv/bin/pip install sqlalchemy numpy bokeh influxdb pysnmp
```

## 一、SQLite + Bokeh

```bash
cd /python_basic/NetDevOps作业/day6_20260420/code
/python_basic/.venv/bin/python day6_1_create_db.py
/python_basic/.venv/bin/python day6_2_write_sqlite.py
/python_basic/.venv/bin/python day6_3_show_sqlite.py
```

生成图表目录：`outputs/`

### SQLite crond

```cron
* * * * * root /python_basic/.venv/bin/python /python_basic/NetDevOps作业/day6_20260420/code/day6_2_write_sqlite.py >> /tmp/day6_sqlite.log 2>&1
```

## 二、InfluxDB + Grafana

```bash
cd /python_basic/NetDevOps作业/day6_20260420/code
docker compose -f docker-compose.yaml up -d
/python_basic/.venv/bin/python day6_4_write_influxdb.py
```

### InfluxDB crond

```cron
* * * * * root /python_basic/.venv/bin/python /python_basic/NetDevOps作业/day6_20260420/code/day6_4_write_influxdb.py >> /tmp/day6_influx.log 2>&1
```

重启并查看日志：

```bash
systemctl restart crond.service
tail -f /tmp/day6_sqlite.log
tail -f /tmp/day6_influx.log
```

Grafana 查询语句见 `grafana.md`。
