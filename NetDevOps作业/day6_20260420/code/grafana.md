# Day6 Grafana 配置

## 数据源

- Type: InfluxDB
- Query Language: InfluxQL
- URL: `http://qyt-influx:8086`（容器内访问）
- Database: `qytdb`
- User: `qytdbuser`
- Password: `Cisc0123`

## Dashboard 面板

### 出向速率 (TX)

```sql
SELECT non_negative_derivative(mean("out_bytes"), 1s) * 8
FROM "interface_monitor"
WHERE $timeFilter
GROUP BY time($__interval), "device_ip", "interface_name"
```

### 入向速率 (RX)

```sql
SELECT non_negative_derivative(mean("in_bytes"), 1s) * 8
FROM "interface_monitor"
WHERE $timeFilter
GROUP BY time($__interval), "device_ip", "interface_name"
```

### Alias By

`[[tag_device_ip]]--[[tag_interface_name]]`

### Unit

`bits/sec (SI)`
