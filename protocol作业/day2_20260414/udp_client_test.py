import socket
import struct
import hashlib
import pickle
def udp_send_data(ip, port, data_list):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id = 1
    for x in data_list:
        send_data = pickle.dumps(x)
        header = struct.pack('!HHIQ', version, pkt_type, seq_id, len(send_data))
        md5_value = hashlib.md5(header + send_data).digest()
        packet = header + send_data + md5_value
        s.sendto(packet, address)
        print(f"发送序列号 {seq_id}: {x}")
        seq_id += 1
    s.close()
if __name__ == "__main__":
    from datetime import datetime
    user_data = ['乾颐堂', [1, 'qytang', 3], {'qytang': 1, 'test': 3}, {'datetime': datetime.now()}]
    udp_send_data('10.10.1.205', 6666, user_data)