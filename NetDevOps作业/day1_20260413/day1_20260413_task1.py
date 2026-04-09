from scapy.all import Ether, ARP, sendp
import time
# 配置参数
iface = "ens33"
target_ip = "10.1.1.1"
source_mac = "00:50:56:a1:8a:72"
# 构造免费ARP Reply包（完整字段）
packet = Ether(src=source_mac, dst="ff:ff:ff:ff:ff:ff") / ARP(
    hwtype=1,          # 硬件类型：以太网
    ptype=0x0800,      # 协议类型：IPv4
    hwlen=6,           # MAC地址长度
    plen=4,            # IP地址长度
    op=2,              # 操作码：Reply
    hwsrc=source_mac,  # 源MAC
    psrc=target_ip,    # 源IP（宣告的IP）
    hwdst=source_mac,  # 目的MAC（=源MAC）
    pdst=target_ip     # 目的IP（=源IP）
)
print(f"持续发送免费ARP Reply到 {target_ip}")
while True:
    sendp(packet, iface=iface, verbose=False)
    print(f"已发送一个ip为{target_ip}、mac为{source_mac}的免费ARP Reply包")
    time.sleep(1)