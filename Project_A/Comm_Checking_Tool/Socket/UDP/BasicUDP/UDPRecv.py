from itertools import count
import socket
import time

ip = ""
port = 9999

data_size = 512

# socket create
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
sock.bind((ip, port))

breakCount = 0
while breakCount < 100:
    data, sender = sock.recvfrom(data_size)
    print("Recv Data : {}, From : {}".format(data, sender))
    breakCount += 1
    time.sleep(0.1)

sock.close()