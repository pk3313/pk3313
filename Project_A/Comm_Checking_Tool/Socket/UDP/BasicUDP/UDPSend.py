import socket
import time

ip = "127.0.0.1"
port = 9999

# connection create
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = "UDP Test..."

breakCount = 0
while breakCount < 100:
    length = send_sock.sendto(data.encode(), (ip, port))
    print("Send Data : {} / Len : {}".format(data, length))
    breakCount += 1
    time.sleep(0.1)

send_sock.close()