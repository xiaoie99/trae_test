from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource
import os
from pathlib import Path
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / 'outputs'
def bokeh_bar(time_list, value_list, line_name,
              title='利用率柱状图', y_label='利用率 (%)', save_name=None):
    """使用 Bokeh 绘制时间序列柱状图 (单设备单指标随时间变化)。"""
    # 根据相邻时间间隔, 自动计算柱宽 (取间隔的 60%, 单位毫秒)
    if len(time_list) > 1:
        delta_ms = (time_list[1] - time_list[0]).total_seconds() * 1000 * 0.6
    else:
        delta_ms = 30000
    source = ColumnDataSource(data={
        'time': time_list,
        'time_str': [t.strftime("%Y-%m-%d %H:%M:%S") for t in time_list],
        'value': value_list
    })
    p = figure(height=400, width=700, title=f"{title} - {line_name}",
               x_axis_type="datetime", x_axis_label='时间', y_axis_label=y_label,
               y_range=(0, 100))
    p.vbar(x='time', top='value', source=source, width=delta_ms,
           color="#e84d60", alpha=0.8, legend_label=line_name)
    hover = HoverTool(tooltips=[("时间", "@time_str"), ("值", "@value%")])
    p.add_tools(hover)
    p.xaxis.formatter = DatetimeTickFormatter(
        minutes="%H:%M", hours="%H:%M", days="%m-%d")
    p.legend.location = "top_right"
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    output_filename = save_name if save_name else str(OUTPUTS_DIR / f"{title}.html")
    output_file(output_filename, title=title)
    save(p)
    print(f"[*] Bokeh 柱状图已生成: {output_filename}")
if __name__ == "__main__":
    # 任务一: 使用随机数据模拟设备CPU利用率，绘制时间序列柱状图
    import random
    from datetime import datetime, timedelta
    # 生成模拟的CPU利用率数据
    print("任务一: 使用 Bokeh 绘制设备性能柱状图")
    print("=" * 50)
    # 生成过去10分钟内的CPU利用率数据，每1分钟一个数据点
    time_list = []
    value_list = []
    # 从当前时间往前推10分钟
    base_time = datetime.now()
    # 生成10个数据点（10分钟，每1分钟一个）
    for i in range(10):
        # 计算时间点
        time_point = base_time - timedelta(minutes=1 * (9 - i))
        time_list.append(time_point)
        # 生成随机CPU利用率（20%-90%之间，模拟真实波动）
        cpu_utilization = random.randint(20, 90)
        value_list.append(cpu_utilization)
    # 显示生成的数据
    print(f"[*] 生成 {len(time_list)} 个数据点")
    print("时间点                CPU利用率")
    print("-" * 30)
    for time_point, utilization in zip(time_list, value_list):
        print(f"{time_point.strftime('%H:%M')}           {utilization}%")
    # 调用bokeh_bar函数绘制柱状图
    print("\n[*] 调用bokeh_bar函数绘制柱状图...")
    # 通过修改save_name参数来确保输出到正确目录，而不修改函数本身
    save_name = str(OUTPUTS_DIR / 'cpu_utilization_bar.html')
    bokeh_bar(time_list, value_list, 'R1 CPU', 
               title='CPU利用率柱状图测试', y_label='利用率 (%)', 
               save_name=save_name)
    print("\n" + "=" * 50)
    print("任务一完成！")
    print("生成的柱状图已保存到: outputs/cpu_utilization_bar.html")
    print("您可以在浏览器中打开该文件查看交互式柱状图")