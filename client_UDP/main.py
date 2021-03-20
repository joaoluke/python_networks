import socket

target_host = '127.0.0.1'
target_port = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((target_host, target_port))
client.sendto('Hello, Server UDP'.encode('utf-8'), (target_host, target_port))

data, addr = client.recvfrom(4096)

print(data, addr)
