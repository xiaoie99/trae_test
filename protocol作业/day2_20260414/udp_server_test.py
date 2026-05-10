import socket
import sys
import struct
import hashlib
import pickle
address = ('0.0.0.0', 6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
print('UDP服务器就绪！等待客户端数据！')
while True:
    try:
        recv_source_data = s.recvfrom(512)
        rdata, addr = recv_source_data
        header = rdata[:16]
        version, pkt_type, seq_id, length = struct.unpack('!HHIQ', header)
        data = rdata[16:16+length]
        md5_recv = rdata[16+length:16+length+16]
        md5_value = hashlib.md5(header + data).digest()
        if md5_recv == md5_value:
            print('=' * 80)
            print("{0:<30}:{1:<30}".format("数据源自于", str(addr)))
            print("{0:<30}:{1:<30}".format("数据库列号", seq_id))
            print("{0:<30}:{1:<30}".format("数据长度为", length))
            print("{0:<30}:{1:<30}".format("数据内容为", str(pickle.loads(data))))
        else:
            print('MD5校验错误！')
    except KeyboardInterrupt:
        sys.exit()