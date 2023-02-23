import socket
import time
udp_ip = "192.168.1.112"
udp_port = 2000

# Recv from NaviPC and send to yourself, send to notebook 
recv_local_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_notebook = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_local_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

recv_local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
send_notebook.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Broadcast socket
send_local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
recv_local_sock.bind(("",udp_port))

while True:
	time.sleep(0.2)
	data, addr = recv_local_sock.recvfrom(4096)
	local_data = send_local_sock.sendto(data,('127.0.0.1',60881))
	notebook_data = send_notebook.sendto(data,('192.168.1.255',60880)) # Broadcast socket
	print("data",data)
	print("local_data",local_data)
	print("notebook_data",notebook_data)
