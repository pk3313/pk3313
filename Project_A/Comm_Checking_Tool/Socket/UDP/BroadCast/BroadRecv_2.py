import socket
import time

port = 60880

data_size = 512

recvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recvSock.bind(('', port))

breakCount = 0
while breakCount < 100:
	recvData, addr = recvSock.recvfrom(data_size)
	print("Recv Data : {}, From : {}".format(recvData, addr))
	breakCount += 1
	time.sleep(0.1)
 
recvSock.close()