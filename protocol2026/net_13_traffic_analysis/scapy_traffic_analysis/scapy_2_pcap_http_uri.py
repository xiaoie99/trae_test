#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import warnings
warnings.filterwarnings("ignore")
from scapy.all import rdpcap, TCP, Raw
import re
import sys
from pathlib import Path

current_file = Path(__file__)
current_root = current_file.parent

sys.path.append(current_root)
from scapy_0_pcap_dir import pcap_dir


def find_pcap_uri(pcap_filename, host_regex):
    # 本代码主要任务: 搜索PCAP文件里边的所有数据包,找到HTTP Host字段匹配正则表达式host_regex的HTTP请求数据包
    # 并收集这个HTTP请求的Host, URI , User_Agent字段
    pkts_file = rdpcap(pcap_filename)  # 使用scapy的rdpcap函数打开pcap文件
    pkt_list = pkts_file.res  # 提取每一个包到清单pkt_list
    result_list = []

    # 原始的HTTP请求报文(packet.getlayer(Raw).fields['load'])大致长这样:
    # 'GET /?nameAccount=4008519651&uid=3102224384&cb=JSONP_CALLBACK_5_61 HTTP/1.1\r\n
    #  Host: hb.crm2.qq.com\r\n
    #  Connection: keep-alive\r\n
    #  Accept: */*\r\n
    #  User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.163.400 QQBrowser/9.3.7175.400\r\n
    #  Referer: http://edu.51cto.com/lecturer/index/user_id-9137368.html\r\n
    #  Accept-Encoding: gzip, deflate, sdch\r\n
    #  Accept-Language: zh-CN,zh;q=0.8\r\n
    #  Cookie: cuid=7780981392; o_cookie=605658506; ...\r\n\r\n'
    #
    # 旧写法 payload.split() 会按所有空白(含空格)切开,导致User-Agent里的空格也被切散,
    # 最终只能取到第一个词 b'Mozilla/5.0'。
    # 新写法改为按\r\n分行,每行再用正则匹配对应首部字段,完整保留值里的空格。

    # ---------- 预编译三条正则, 分别负责HTTP请求行 / Host首部 / User-Agent首部 ----------
    # 说明:
    # 1) rb'...' 表示 raw bytes, 因为scapy给到的payload是bytes(b'...'), 所以正则也要用bytes模式
    # 2) ^ 和 $ 分别匹配"一行的开头"和"一行的结尾"(这里每次只对一行做match,所以等价于行首/行尾)
    # 3) \s 表示空白(空格/制表符等); \s* 表示零个或多个空白; \s+ 表示至少一个空白
    # 4) (.+?) 是"非贪婪"捕获组,尽量少地匹配字符,配合末尾的 \s*$ 就能把值两端的空白吃掉
    # 5) re.IGNORECASE 让首部名大小写都能匹配(Host/host/HOST 都可以)

    # 请求行示例: b'GET /abc?x=1 HTTP/1.1'
    #   ^(?:GET|POST|...)   —— 行首必须是这些方法之一; (?:...) 是"非捕获组",只用来分组不抓取
    #   \s+(\S+)\s+HTTP/    —— 方法后跟空格, 然后捕获"非空白"的URI(group 1), 再跟空格和 HTTP/
    request_line_re = re.compile(rb'^(?:GET|POST|HEAD|PUT|DELETE|OPTIONS)\s+(\S+)\s+HTTP/', re.IGNORECASE)

    # Host首部示例: b'Host: www.sina.com.cn'
    #   ^Host:\s*  —— 行首 'Host:' 后可带零个或多个空白(通常是一个空格)
    #   (.+?)      —— 非贪婪地捕获Host的值(group 1), 比如 www.sina.com.cn
    #   \s*$       —— 吃掉末尾可能残留的空白, 保证值干净
    host_re = re.compile(rb'^Host:\s*(.+?)\s*$', re.IGNORECASE)

    # User-Agent首部示例:
    #   b'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ...'
    # 用 (.+?)\s*$ 可以把整行(含内部空格)完整抓下来,这正是之前split()丢失空格的症结
    user_agent_re = re.compile(rb'^User-Agent:\s*(.+?)\s*$', re.IGNORECASE)

    # ---------- 逐个数据包解析 ----------
    for packet in pkt_list:
        try:
            # 只看发往80端口的TCP包(客户端到Web服务器的HTTP请求方向)
            if packet.getlayer(TCP).fields['dport'] != 80:
                continue

            # Raw层是TCP载荷(也就是HTTP报文本身); 三次握手纯SYN/ACK包没有Raw层,要跳过
            raw_layer = packet.getlayer(Raw)
            if raw_layer is None:
                continue

            # payload 是一整段bytes, HTTP头之间用 \r\n 分隔, 头和空体之间是 \r\n\r\n
            payload = raw_layer.fields['load']

            # 按 \r\n 切成"每一行一个元素"的列表, 这样每个首部就是独立的一行, 便于正则匹配
            # 例如: [b'GET / HTTP/1.1', b'Host: a.com', b'User-Agent: Mozilla/5.0 (...)', b'', ...]
            lines = payload.split(b'\r\n')

            # 先把三个目标字段初始化为None, 边扫边填
            uri = host = user_agent = None
            for line in lines:
                # 对当前这一行依次尝试三条正则; .match() 只从行首开始匹配, 匹配不上返回None
                # 每个字段拿到一次就不再重复匹配(if ... is None 守卫)
                if uri is None:
                    m = request_line_re.match(line)
                    if m:
                        uri = m.group(1)  # group(1) 就是正则里第一个(...)捕获到的内容
                        continue
                if host is None:
                    m = host_re.match(line)
                    if m:
                        host = m.group(1)
                        continue
                if user_agent is None:
                    m = user_agent_re.match(line)
                    if m:
                        user_agent = m.group(1)
                        continue
                # 三个都拿到了就不必再看后面的首部(Cookie/Referer等), 直接跳出
                if uri and host and user_agent:
                    break

            # 没有Host或URI通常说明这个包不是HTTP请求(可能是响应或乱序TCP分片), 跳过
            if not host or not uri:
                continue
            # host必须匹配外层传入的正则(例如 r'sina\.com\.cn'), 不匹配就不收集
            # host是bytes, 正则host_regex是str, 所以先decode一下; errors='ignore' 防止偶发非法字节报错
            if not re.search(host_regex, host.decode(errors='ignore')):
                continue
            # 有些请求没有User-Agent首部, 给个占位符, 避免后面 print 拼接时出错
            if user_agent is None:
                user_agent = b'-'

            result_list.append((host, uri, user_agent))
        except Exception:
            # 解析单个包失败不影响整体, 继续下一个包
            pass
    return result_list


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    result = find_pcap_uri(pcap_dir + "dos.pcap", r'sina\.com\.cn')

    # 对找到数据包进行展示,打印Host, URI , User_Agent
    i = 1
    for http_info in result:
        print('=' * 30 + str(i) + '=' * 30)
        print(b'Host: ' + http_info[0])
        print(b'URI: ' + http_info[1])
        print(b'User_Agent: ' + http_info[2])
        i += 1

    # 展示所有host, 使用集合技术, 去除重复部分
    host_list = []
    for http_info in result:
        host_list.append(http_info[0])
    print('=' * 62)
    print(host_list)
    print([i.decode() for i in list(set(host_list))])  # 使用集合技术,找到不重复的Host
