import socket
import time

ip = "192.168.1.123"
port = 5017

# socket create and connection
send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_sock.connect((ip, port))

# send msg
test_msg = "TCP Test..."

breakCount = 0
while breakCount < 100:
    length = send_sock.send(test_msg.encode())
    print("Send Data : {}, Len : {}".format(test_msg, length))
    breakCount += 1
    time.sleep(0.1)

# connection close
send_sock.close()