#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.plotting import figure, output_file, save
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"
LINE_COLORS = ["red", "blue", "green", "orange", "purple", "brown", "black"]
def bokeh_line(lines_data, title="接口速率测试", y_label="速率 (kbps)", save_name=None):
    p = figure(
        height=430,
        width=900,
        title=title,
        x_axis_type="datetime",
        x_axis_label="时间",
        y_axis_label=y_label,
    )
    for i, (time_list, value_list, line_name) in enumerate(lines_data):
        color = LINE_COLORS[i % len(LINE_COLORS)]
        source = ColumnDataSource(
            data={
                "time": time_list,
                "time_str": [t.strftime("%Y-%m-%d %H:%M:%S") for t in time_list],
                "value": value_list,
            }
        )
        p.line(x="time", y="value", source=source, line_width=2, color=color, legend_label=line_name)
        p.scatter(x="time", y="value", source=source, size=5, color=color, alpha=0.6)
    hover = HoverTool(tooltips=[("时间", "@time_str"), ("值", "@value kbps")], mode="vline")
    p.add_tools(hover)
    p.xaxis.formatter = DatetimeTickFormatter(minutes="%H:%M", hours="%H:%M", days="%m-%d")
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    output_filename = save_name if save_name else str(OUTPUTS_DIR / f"{title}.html")
    output_file(output_filename, title=title)
    save(p)
    print(f"[*] Bokeh 折线图已生成: {output_filename}")
if __name__ == "__main__":
    # 工具函数测试输出 (bokeh_line 单独运行): 仅 10.10.1.200 Gi1，RX/TX 同图
    from datetime import datetime, timedelta
    import random
    ip = "10.10.1.200"
    iface = "Gi1"
    n = 12
    base = datetime.now().replace(second=0, microsecond=0)
    times = [base - timedelta(minutes=n - 1 - i) for i in range(n)]
    def fake_kbps(seed: int) -> list:
        rnd = random.Random(seed)
        return [round(50 + rnd.random() * 800, 2) for _ in range(n)]
    print("工具函数测试输出 (bokeh_line 单独运行): 10.10.1.200 Gi1 RX/TX 模拟")
    lines_data = [
        [times, fake_kbps(200), f"RX:{ip}:{iface}"],
        [times, fake_kbps(1200), f"TX:{ip}:{iface}"],
    ]
    bokeh_line(lines_data, title="接口速率测试", y_label="速率 (kbps)")
