import socket
import time

MCAST_GRP = '239.0.1.49'
MCAST_PORT = 2000

# 멀티캐스트의 홉 (가입자 수)
MULTICAST_TTL = 2

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

data = "MultiCast Test..."

breakCount = 0
while breakCount < 100:
    length = send_sock.sendto(data.encode(), (MCAST_GRP, MCAST_PORT))
    print("Send Data : {}, Len : {}".format(data, length))
    breakCount += 1
    time.sleep(0.1)

send_sock.close()