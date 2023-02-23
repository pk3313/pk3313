import socket
import struct
import time

MCAST_GRP = '239.0.1.49'
MCAST_PORT = 2000
IS_ALL_GROUP =True

ip = '192.168.1.121'

data_size = 512

recvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
recvSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if IS_ALL_GROUP:
    recvSock.bind(("", MCAST_PORT)) # 모든 멀티캐스트 그룹을 수신하는 경우
    # recvSock.bind((ip, MCAST_PORT)) # 특정 멀티캐스트 그룹을 수신하는 경우
else:
    recvSock.bind((MCAST_GRP,MCAST_PORT))

mreq = struct.pack("4sl",socket.inet_aton(MCAST_GRP),socket.INADDR_ANY)
recvSock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

breakCount = 0
while breakCount < 100:
    data, sender = recvSock.recvfrom(data_size)
    print("Recv Data : {}, From : {}".format(data, sender))
    breakCount += 1
    time.sleep(0.1)

recvSock.close()