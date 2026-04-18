import re
from tools.day3_ssh_single_cmd import ssh_run
from tools.day3_bokeh_bing import bokeh_bing
def get_netflow_app(host, username, password):
    """SSH登录路由器, 采集Netflow数据, 正则提取, 绘制Bokeh饼状图。"""
    # 1. SSH执行命令获取Netflow数据
    show_result = ssh_run(host, username, password, 'show flow monitor name qytang-monitor cache format table')
    print(show_result)
    # 2. 正则提取APP NAME和bytes
    app_name_list = []
    app_bytes_list = []
    for line in show_result.strip().split('\n'):
        # 匹配格式: "layer7 mdns                            24464"
        # 使用正则表达式匹配前缀(port/layer7/prot) + 空格 + 应用名 + 多个空格 + 数字
        match = re.match(r'^(\w+\s+\w+)\s+(\d+)$', line.strip())
        if match:
            app_name = match.group(1)
            app_bytes = match.group(2)
            # 过滤掉表头行
            if app_name.lower() != 'app name' and app_name.lower() != '========':
                app_name_list.append(app_name)
                app_bytes_list.append(app_bytes)
    # 3. 按照期望格式打印提取结果
    print(f"[*] 提取到 {len(app_name_list)} 条 Netflow 记录")
    for name, byt in zip(app_name_list, app_bytes_list):
        print(f"    {name:<25s} {byt} bytes")
    # 4. 调用bokeh_bing生成饼状图
    bokeh_bing(app_name_list, app_bytes_list, 'Netflow应用流量分布')
if __name__ == "__main__":
    get_netflow_app('10.10.1.200', 'admin', 'qwert@12345')