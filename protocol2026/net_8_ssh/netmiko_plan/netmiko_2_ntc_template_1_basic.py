import os
from textfsm import clitable
import sys
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_dir = current_file.parent
sys.path.append(str(current_dir))

from netmiko_1_show_client import netmiko_show_cred, device_ip, username, password
from ntc_templates.parse import parse_output



def clitable_to_dict(cli_table):
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        objs.append(temp_dict)
    if len(objs) == 1:
        return objs[0]  # 只有一条记录，返回字典
    else:
        return objs  # 多条记录，返回列表


def netmiko_ntc_template(ip, username, password, cmd, device_type):
    # 第1步：通过Netmiko执行命令，先拿到设备返回的原始文本输出
    # 后续所有结构化解析都基于这段ssh_output进行处理
    ssh_output = netmiko_show_cred(ip, username, password, cmd, device_type)

    # 第2步：优先加载项目内自定义模板目录
    # 这里使用 `index` 作为模板索引文件名，目录指向当前脚本同级的 `ntc-template`
    # 这样可以优先匹配你自己维护的模板规则，而不是直接依赖系统模板
    custom_template_path = f'{current_dir}{os.sep}ntc-template'
    cli_table = clitable.CliTable('index', custom_template_path)

    # 第3步：构造TextFSM模板匹配条件
    # Command 对应命令关键字，Vendor 对应平台（如 cisco_ios）
    # index 文件会根据这两个字段决定具体使用哪个模板
    attributes = {'Command': cmd, 'Vendor': device_type}

    try:
        # 第4步（主路径）：先尝试用自定义模板解析
        # 解析成功时，结果先是CliTable对象，再转换为更易用的dict/list结构返回
        cli_table.ParseCmd(ssh_output, attributes)
        parse_result = clitable_to_dict(cli_table)
    except Exception as e:
        # 第5步（回退路径1）：自定义模板失败时，回退到系统安装的 ntc_templates.parse_output
        # 这个方法通常依赖 pip 安装的 ntc-templates 模板库
        try:
            parse_result = parse_output(platform=device_type,
                                        command=cmd,
                                        data=ssh_output)
            # 系统模板虽然调用成功，但可能没匹配到有效字段（返回空）
            # 这种情况下返回原始输出，避免调用方拿到空结果
            if not parse_result:
                parse_result = ssh_output
        # 第6步（回退路径2）：如果系统模板也失败，最终兜底返回原始CLI输出
        # 这样无论模板是否可用，函数都能保证有可读结果，不会中断主流程
        except Exception as e:
            return ssh_output

    return parse_result


if __name__ == "__main__":
    from pprint import pprint
    pprint(netmiko_ntc_template(device_ip,
                                'admin',
                                'Cisc0123',
                                'show ip inter brie',
                                # 'show version',
                                # 'show interface',
                                # "show run | in username",
                                # 'show flash:',  # 要打印正常需要普通的ping
                                'cisco_ios')
           )
