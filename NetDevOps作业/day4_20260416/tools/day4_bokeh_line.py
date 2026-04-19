from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource
import os
from pathlib import Path
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / 'outputs'
LINE_COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
def bokeh_line(lines_data, title='利用率趋势', y_label='利用率 (%)', save_name=None):
    """
    使用 Bokeh 绘制多条折线的时间序列图。
    :param lines_data: 多条线的数据列表, 格式:
        [[time_list, value_list, line_name], [time_list, value_list, line_name], ...]
    :param title:   图表标题
    :param y_label: Y轴标签
    :param save_name: 输出文件路径, None 则自动保存到 outputs/{title}.html
    """
    p = figure(height=400, width=700, title=title,
               x_axis_type="datetime", x_axis_label='时间', y_axis_label=y_label,
               y_range=(0, 100))
    for i, (time_list, value_list, line_name) in enumerate(lines_data):
        color = LINE_COLORS[i % len(LINE_COLORS)]
        source = ColumnDataSource(data={
            'time': time_list,
            'time_str': [t.strftime("%Y-%m-%d %H:%M:%S") for t in time_list],
            'value': value_list
        })
        p.line(x='time', y='value', source=source, line_width=2,
               color=color, legend_label=line_name)
        p.scatter(x='time', y='value', source=source, size=5,
                  color=color, alpha=0.5)
    hover = HoverTool(tooltips=[("时间", "@time_str"), ("值", "@value%")], mode='vline')
    p.add_tools(hover)
    p.xaxis.formatter = DatetimeTickFormatter(
        minutes="%H:%M",
        hours="%H:%M",
        days="%m-%d"
    )
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    output_filename = save_name if save_name else str(OUTPUTS_DIR / f"{title}.html")
    output_file(output_filename, title=title)
    save(p)
    print(f"[*] Bokeh 折线图已生成: {output_filename}")
if __name__ == "__main__":
    # 任务二: 使用随机数据模拟多设备性能趋势，绘制时间序列折线图
    import random
    from datetime import datetime, timedelta
    # 生成模拟的多设备CPU利用率数据
    print("任务二: 使用 Bokeh 绘制多设备性能趋势图")
    print("=" * 50)
    # 模拟2台设备的CPU利用率数据
    lines_data = []
    device_names = ["R1", "R2"]
    # 从当前时间往前推10分钟
    base_time = datetime.now()
    for device_name in device_names:
        time_list = []
        value_list = []
        # 生成10个数据点（10分钟，每1分钟一个）
        for i in range(10):
            # 计算时间点
            time_point = base_time - timedelta(minutes=1 * (9 - i))
            time_list.append(time_point)
            # 生成随机CPU利用率（20%-70%之间，模拟真实波动）
            cpu_utilization = random.randint(20, 70)
            value_list.append(cpu_utilization)
        # 添加到lines_data
        lines_data.append([time_list, value_list, f"{device_name} CPU"])
        # 显示生成的数据
        print(f"\n[*] {device_name} - 生成 {len(time_list)} 个数据点")
        print("时间点                CPU利用率")
        print("-" * 30)
        for time_point, utilization in zip(time_list, value_list):
            print(f"{time_point.strftime('%H:%M')}           {utilization}%")
    # 调用bokeh_line函数绘制折线图
    print("\n[*] 调用bokeh_line函数绘制折线图...")
    # 通过修改save_name参数来确保输出到正确目录
    save_name = str(OUTPUTS_DIR / 'multi_device_cpu_trend.html')
    bokeh_line(lines_data, 
               title='CPU利用率线形图测试', y_label='利用率 (%)', 
               save_name=save_name)
    print("\n" + "=" * 50)
    print("任务二完成！")
    print("生成的折线图已保存到: outputs/multi_device_cpu_trend.html")
    print("您可以在浏览器中打开该文件查看交互式折线图")