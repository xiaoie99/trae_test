#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime, timedelta, timezone

from pymongo import MongoClient
import plotly.graph_objects as go
import plotly.io as pio


# ---------- Mongo Helpers ----------

def get_mongo_client() -> MongoClient:
	mongo_host = os.environ.get('MONGO_HOST', 'localhost')
	mongo_port = int(os.environ.get('MONGO_PORT', '27017'))
	return MongoClient(host=mongo_host, port=mongo_port)


def get_collection(client: MongoClient):
	db_name = os.environ.get('MONGO_DB', 'netflowdb')
	coll_name = os.environ.get('MONGO_COLLECTION', 'flows')
	return client[db_name][coll_name]


# ---------- Time Range ----------

RANGE_MAP = {
	"15m": 15,
	"30m": 30,
	"1h": 60,
	"3h": 180,
	"6h": 360,
	"24h": 1440,
}


def make_time_filter(range_key: str) -> Dict:
	minutes = RANGE_MAP.get(range_key, 60)
	since = datetime.now(timezone.utc) - timedelta(minutes=minutes)
	return {"collector_received_at": {"$gte": since}}


# choose bucket (seconds) based on range
BUCKET_SEC = {
	"15m": 60,
	"30m": 60,
	"1h": 60,
	"3h": 300,
	"6h": 300,
	"24h": 900,
}


def bucket_params(range_key: str) -> Tuple[str, int]:
	# use Mongo dateTrunc unit minute with binSize derived from seconds
	sec = BUCKET_SEC.get(range_key, 60)
	if sec % 3600 == 0:
		return ("hour", sec // 3600)
	elif sec % 60 == 0:
		return ("minute", sec // 60)
	else:
		return ("second", sec)


# ---------- Dynamic Protocol / Service Map ----------

def load_protocol_map() -> Dict[int, str]:
	proto_name: Dict[int, str] = {1: 'ICMP', 2: 'IGMP', 6: 'TCP', 17: 'UDP'}
	file_path = os.environ.get('PROTOCOL_MAP_FILE') or str(Path(__file__).parent / 'config' / 'protocol_map.json')
	try:
		p = Path(file_path)
		if p.exists():
			data = json.loads(p.read_text(encoding='utf-8'))
			for k, v in data.items():
				try:
					proto_name[int(k)] = str(v)
				except Exception:
					continue
	except Exception:
		pass
	env_map = os.environ.get('PROTOCOL_MAP', '').strip()
	if env_map:
		pairs = [x for x in env_map.split(',') if ':' in x]
		for pair in pairs:
			k, v = pair.split(':', 1)
			try:
				proto_name[int(k.strip())] = v.strip()
			except Exception:
				continue
	return proto_name


def load_service_map() -> Dict[str, str]:
	"""Return mapping for application names.
	Key preferred format: "<proto>/<port>", e.g., "6/443"; also supports port-only key, e.g., "443".
	Load order: env SERVICE_MAP -> json SERVICE_MAP_FILE -> built-in defaults.
	"""
	service_map: Dict[str, str] = {
		"6/22": "SSH",
		"6/23": "Telnet",
		"6/25": "SMTP",
		"17/53": "DNS",
		"6/80": "HTTP",
		"6/110": "POP3",
		"6/143": "IMAP",
		"17/123": "NTP",
		"6/443": "HTTPS",
		"17/161": "SNMP",
		"17/162": "SNMP Trap",
		"17/2055": "NetFlow",
		"17/514": "Syslog",
		"17/69": "TFTP",
		"6/1521": "Oracle TNS",
		"6/3306": "MySQL",
		"6/3389": "RDP",
		"6/5432": "PostgreSQL",
		"6/6379": "Redis",
		"6/27017": "MongoDB",
		"80": "HTTP",
		"443": "HTTPS",
		"22": "SSH",
		"25": "SMTP",
		"53": "DNS",
	}
	file_path = os.environ.get('SERVICE_MAP_FILE') or str(Path(__file__).parent / 'config' / 'service_map.json')
	try:
		p = Path(file_path)
		if p.exists():
			data = json.loads(p.read_text(encoding='utf-8'))
			for k, v in data.items():
				service_map[str(k).strip()] = str(v)
	except Exception:
		pass
	env_map = os.environ.get('SERVICE_MAP', '').strip()
	if env_map:
		pairs = [x for x in env_map.split(',') if ':' in x]
		for pair in pairs:
			k, v = pair.split(':', 1)
			service_map[k.strip()] = v.strip()
	return service_map


def resolve_app_name(proto: int, port: int, proto_map: Dict[int, str], svc_map: Dict[str, str]) -> str:
	key_full = f"{proto}/{port}"
	if key_full in svc_map:
		return svc_map[key_full]
	if str(port) in svc_map:
		return svc_map[str(port)]
	pname = proto_map.get(proto, f"PROTO({proto})")
	if pname in ("TCP", "UDP"):
		return f"{pname}/{port}"
	return pname


# ---------- Queries ----------

def query_app_distribution(range_key: str, top_n: int = 10) -> List[Tuple[str, int]]:
	client = get_mongo_client()
	try:
		coll = get_collection(client)
		match = make_time_filter(range_key)
		pipeline = [
			{"$match": match},
			{"$group": {
				"_id": {"proto": "$fields.PROTOCOL", "dport": {"$ifNull": ["$fields.L4_DST_PORT", 0]}},
				"bytes": {"$sum": {"$ifNull": ["$fields.IN_BYTES", 0]}}
			}},
			{"$sort": {"bytes": -1}}
		]
		rows = list(coll.aggregate(pipeline, allowDiskUse=True))
		proto_map = load_protocol_map()
		svc_map = load_service_map()
		agg: Dict[str, int] = {}
		for r in rows:
			proto = r.get('_id', {}).get('proto')
			port = r.get('_id', {}).get('dport')
			b = int(r.get('bytes', 0))
			name = resolve_app_name(proto, port, proto_map, svc_map)
			agg[name] = agg.get(name, 0) + b
		items = sorted(agg.items(), key=lambda x: x[1], reverse=True)
		labels: List[str] = []
		values: List[int] = []
		others = 0
		for idx, (name, b) in enumerate(items):
			if idx < top_n:
				labels.append(name)
				values.append(b)
			else:
				others += b
		if items and others > 0:
			labels.append('Others')
			values.append(others)
		return list(zip(labels, values))
	finally:
		client.close()


def query_top_talkers(range_key: str, limit: int = 10) -> List[Tuple[str, int]]:
	client = get_mongo_client()
	try:
		coll = get_collection(client)
		match = make_time_filter(range_key)
		pipeline = [
			{"$match": match},
			{"$addFields": {"src": {"$ifNull": ["$fields.IPV4_SRC_ADDR", "$fields.IPV6_SRC_ADDR"]}}},
			{"$match": {"src": {"$type": "string"}}},
			{"$group": {"_id": "$src", "bytes": {"$sum": {"$ifNull": ["$fields.IN_BYTES", 0]}}}},
			{"$sort": {"bytes": -1}},
			{"$limit": int(limit)}
		]
		rows = list(coll.aggregate(pipeline, allowDiskUse=True))
		return [(r.get('_id'), int(r.get('bytes', 0))) for r in rows]
	finally:
		client.close()


def query_timeseries_bps(range_key: str) -> Tuple[List[str], List[float], str]:
	"""Return (timestamps_iso, values_scaled, unit_str)."""
	client = get_mongo_client()
	try:
		coll = get_collection(client)
		match = make_time_filter(range_key)
		unit, binsize = bucket_params(range_key)
		pipeline = [
			{"$match": match},
			{"$group": {
				"_id": {"$dateTrunc": {"date": "$collector_received_at", "unit": unit, "binSize": binsize}},
				"bytes": {"$sum": {"$ifNull": ["$fields.IN_BYTES", 0]}}
			}},
			{"$sort": {"_id": 1}}
		]
		rows = list(coll.aggregate(pipeline, allowDiskUse=True))
		bucket_seconds = BUCKET_SEC.get(range_key, 60)
		times: List[str] = []
		bps_list: List[float] = []
		for r in rows:
			ts = r.get('_id')
			b = int(r.get('bytes', 0))
			bps = (b * 8) / bucket_seconds if bucket_seconds else 0
			times.append(ts.isoformat())
			bps_list.append(bps)
		# choose unit
		maxv = max(bps_list) if bps_list else 0
		if maxv >= 1e9:
			scale, unit_label = 1e9, 'Gbps'
		elif maxv >= 1e6:
			scale, unit_label = 1e6, 'Mbps'
		elif maxv >= 1e3:
			scale, unit_label = 1e3, 'Kbps'
		else:
			scale, unit_label = 1.0, 'bps'
		values_scaled = [v / scale for v in bps_list]
		return times, values_scaled, unit_label
	finally:
		client.close()


# ---------- Styling helpers ----------

PALETTE = [
	"#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#17BECF", "#BCBD22", "#9467BD", "#8C564B",
	"#E377C2", "#7F7F7F", "#AEC7E8", "#FFBB78", "#98DF8A", "#FF9896", "#C5B0D5", "#C49C94"
]

FONT_FAMILY = "Inter, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans SC', 'Microsoft YaHei', sans-serif"


def apply_palette(fig: go.Figure, n: int) -> None:
	colors = (PALETTE * ((n // len(PALETTE)) + 1))[:n]
	fig.update_traces(marker=dict(colors=colors, line=dict(color="#ffffff", width=1)))


def style_fig(fig: go.Figure, title: str) -> go.Figure:
	fig.update_layout(
		title_text=title,
		font=dict(family=FONT_FAMILY, size=14, color="#111827"),
		title_font=dict(family=FONT_FAMILY, size=22, color="#0F172A", weight=700),
		legend=dict(orientation='h', y=-0.12, font=dict(size=12)),
		uniformtext_minsize=10,
		uniformtext_mode='hide',
		margin=dict(l=10, r=10, t=50, b=10),
		autosize=True,
		height=520,
		paper_bgcolor="#ffffff",
		plot_bgcolor="#ffffff",
	)
	return fig


def build_pie(title: str, labels: List[str], values: List[int]) -> go.Figure:
	labels = labels or ['No Data']
	values = values or [1]
	fig = go.Figure(data=[go.Pie(
		labels=labels,
		values=values,
		hole=0,
		sort=False,
		direction='clockwise',
		textposition='inside',
		textinfo='percent',
		insidetextorientation='horizontal',
		showlegend=True
	)])
	apply_palette(fig, len(labels))
	return style_fig(fig, title)


def build_app_distribution_figure(data: List[Tuple[str, int]]) -> go.Figure:
	labels = [x[0] for x in data]
	values = [x[1] for x in data]
	return build_pie('应用分布（按字节）', labels, values)


def build_top_talkers_figure(data: List[Tuple[str, int]]) -> go.Figure:
	labels = [x[0] for x in data]
	values = [x[1] for x in data]
	return build_pie('Top Talkers（按字节）', labels, values)


def build_timeseries_figure(times: List[str], values: List[float], unit_label: str) -> go.Figure:
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=times, y=values, mode='lines+markers', line=dict(color='#1F77B4', width=2)))
	fig.update_layout(
		title_text=f'总速率（{unit_label}）',
		xaxis_title='时间',
		yaxis_title=unit_label,
		font=dict(family=FONT_FAMILY, size=14, color="#111827"),
		title_font=dict(family=FONT_FAMILY, size=22, color="#0F172A", weight=700),
		margin=dict(l=10, r=10, t=50, b=10),
		height=420,
		paper_bgcolor="#ffffff",
		plot_bgcolor="#ffffff",
	)
	return fig


# ---------- HTML ----------

def generate_report_html(range_key: str = '1h') -> str:
	times, values, unit_label = query_timeseries_bps(range_key)
	app_data = query_app_distribution(range_key)
	talker_data = query_top_talkers(range_key, 10)

	line_fig = build_timeseries_figure(times, values, unit_label)
	app_fig = build_app_distribution_figure(app_data)
	talker_fig = build_top_talkers_figure(talker_data)

	line_div = pio.to_html(line_fig, include_plotlyjs=False, full_html=False,
							config={"responsive": True}, default_width="100%", default_height="420px")
	app_div = pio.to_html(app_fig, include_plotlyjs='inline', full_html=False,
							config={"responsive": True}, default_width="100%", default_height="520px")
	talker_div = pio.to_html(talker_fig, include_plotlyjs=False, full_html=False,
							config={"responsive": True}, default_width="100%", default_height="520px")

	html = f"""
<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
	<meta charset=\"UTF-8\" />
	<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
	<title>NetFlow 分析（实时查询 MongoDB）</title>
	<style>
		:root {{ --title-color: #0F172A; --muted: #6B7280; }}
		body {{ font-family: {FONT_FAMILY}; margin: 0; background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%); color: #111827; }}
		.container {{ max-width: 1280px; margin: 0 auto; padding: 20px 20px 24px; }}
		h1 {{ font-size: 30px; font-weight: 800; color: var(--title-color); margin: 4px 0 6px 0; text-align: center; }}
		.toolbar {{ display:flex; gap:8px; justify-content:center; align-items:center; margin: 8px 0 16px; }}
		.range-btn {{ padding:6px 10px; border:1px solid #E5E7EB; border-radius:8px; background:#fff; cursor:pointer; font-size:13px; color:#111827; text-decoration:none; }}
		.range-btn.active {{ background:#111827; color:#fff; border-color:#111827; }}
		.row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: stretch; }}
		.card {{ border: 1px solid #E5E7EB; border-radius: 12px; padding: 10px; box-shadow: 0 6px 16px rgba(15,23,42,0.06); background: #fff; min-height: 560px; }}
		.card-wide {{ grid-column: 1 / -1; border: 1px solid #E5E7EB; border-radius: 12px; padding: 10px; box-shadow: 0 6px 16px rgba(15,23,42,0.06); background: #fff; min-height: 440px; margin-bottom: 16px; }}
		.js-plotly-plot, .plot-container, .svg-container {{ width: 100% !important; }}
		@media (max-width: 1200px) {{ .row {{ grid-template-columns: 1fr; }} }}
	</style>
</head>
<body>
	<div class=\"container\">
		<h1>NetFlow 分析（实时查询 MongoDB）</h1>
		<div class=\"toolbar\">
			<span style=\"font-size:13px;color:#6B7280\">时间范围：</span>
			<a class=\"range-btn { 'active' if range_key=='15m' else '' }\" href=\"/?range=15m\">15分钟</a>
			<a class=\"range-btn { 'active' if range_key=='30m' else '' }\" href=\"/?range=30m\">30分钟</a>
			<a class=\"range-btn { 'active' if range_key=='1h' else '' }\" href=\"/?range=1h\">1小时</a>
			<a class=\"range-btn { 'active' if range_key=='3h' else '' }\" href=\"/?range=3h\">3小时</a>
			<a class=\"range-btn { 'active' if range_key=='6h' else '' }\" href=\"/?range=6h\">6小时</a>
			<a class=\"range-btn { 'active' if range_key=='24h' else '' }\" href=\"/?range=24h\">24小时</a>
		</div>
		<div class=\"row\">
			<div class=\"card\">{app_div}</div>
			<div class=\"card\">{talker_div}</div>
		</div>
		<div class=\"card-wide\">{line_div}</div>
	</div>
	<script>
		window.addEventListener('load', function () {{
			setTimeout(function() {{ window.dispatchEvent(new Event('resize')); }}, 150);
		}});
	</script>
</body>
</html>
"""
	return html


if __name__ == '__main__':
	report_html = generate_report_html('1h')
	out_path = Path(__file__).parent / 'report.html'
	out_path.write_text(report_html, encoding='utf-8')
	print(str(out_path))
