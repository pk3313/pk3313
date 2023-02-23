import socket
import time
import os

ip = '192.168.0.255'
port = 60880

# dirName = os.path.dirname(os.path.realpath(__file__))
f = open("data.txt", 'r')
data = f.read()

# data = 'BroadCast Test...'

sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

breakCount = 0
# while breakCount < 100:
while True:
	length = sendSock.sendto(data.encode(), (ip, port))
	print("Send Data : {}, Len : {}".format(data, length))
	breakCount += 1
	time.sleep(0.1)

sendSock.close()