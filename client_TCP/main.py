import socket

target_host = '127.0.0.1'
target_port = 4160

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

data = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
client.send(data.encode('utf-8'))
response = client.recv(4096).decode('utf-8')

print(response)
