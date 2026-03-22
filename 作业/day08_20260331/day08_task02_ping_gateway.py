from pythonping import ping
# 定义函数
def ping_check(host):
    result = ping(host, count=1, timeout=2)
    if result.success():
        return True, result.rtt_avg_ms
    else:
        return False, None
# 主程序
if __name__ == '__main__':
    gateways = ['196.21.5.1', '10.0.0.1', '172.16.1.1' , '10.10.1.254']
    for gateway in gateways:
        reachable, rtt = ping_check(gateway)
        if reachable:
            print("{:<12}: 可达   | RTT: {:.2f} ms".format(gateway, rtt))
        else:
            print("{:<12}: 不可达".format(gateway))