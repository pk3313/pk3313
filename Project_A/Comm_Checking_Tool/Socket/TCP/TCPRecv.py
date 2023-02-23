import socket
import time

ip = "0.0.0.0"
port = 5017

BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recv_address = ('0.0.0.0', port)
sock.bind(recv_address)

sock.listen(1)
 
conn, addr = sock.accept()

# recv and send loop
breakCount = 0
while breakCount < 100:
    data = conn.recv(BUFFER_SIZE)
    print("Recv Data : {}".format(data))
    breakCount += 1
    time.sleep(0.1)

conn.close()