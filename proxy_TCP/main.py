import sys
import socket
import threading


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print('[!!] Failed to listen on %s:%d' % (local_host, local_port))
        print('[!!] Check for other listening sockets or correct permissions.')
    
    print('[*] Listening on %s:%d' % (local_host, local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # Exibe informações sobre a conexão local
        print('[==>] Received incoming connection from %s:%d' % (addr[0], addr[1]))

        # Inicia uma thread para conversar com o host remoto
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

def main():
    # Sem parsing sofisticado de linha de comando nesse caso
    if len(sys.argv[1:]) != 5:
        print("Usage: ./main.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print('Example: ./main.py 127.0.0.1 9000 10.12.132.1 9000 True')
        sys.exit(0)
    
    # Define parâmentros para ouvir localmente
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # Define o alvo remoto
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # O código a seguir diz ao nosso proxy para conectar e receber dados
    # antes de enviar ao host remoto
    receive_first = sys.argv[5]

    if "True" in receive_first: 
        receive_first = True
    else:
        receive_first = False

    # Agora coloca em ação o nosso socket que ficará ouvindo
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

main()