import socket
import threading

bind_ip = '127.0.0.1'
bind_port = 4160

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(1)

print('[*] Listening on %s:%d' % (bind_ip, bind_port))


# Thread para tratamento de clientes
def handle_client(client_socket):
    # Exibe o que o cliente enviar
    request = client_socket.recv(1024)
    print('[*] Received: %s' % request)

    # Envia um pacote de volta
    mesage = 'ARK!'
    client_socket.send(mesage.encode('utf-8'))
    client_socket.close()


while True:
    client, addr = server.accept()
    print('[*] Accepted connection from: %s:%d' % (addr[0], addr[1]))

    # Coloca nossa Thread de cliente em ação para tratar dados de entrada
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
