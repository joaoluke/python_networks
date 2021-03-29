import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((local_host,local_port))
        
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)
        
    
    print "[*] Listening on %s:%d" % (local_host, local_port)
    
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # Exibe informacoes sobre a conexao local
        print "[==>] Received incoming connection from %s:%d" % (addr[0],addr[1])
        
        # Inicia uma thread para conversar com o host remoto
        proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        
        
        proxy_thread.start()
        

def proxy_handler(client_socket, remote_host,remote_port,receive_first):
    
    # Conecta ao host remoto
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    remote_socket.connect((remote_host,remote_port))
    
    
    # Recebe dados do lado remoto se necessario
    if receive_first:
        
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        
        
        # Envia os dados ao nosso handler de resposta
        remote_buffer = response_handler(remote_buffer)
        
        
        # Se houver dados para serem enviados ao nosso cliente local envia-os
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
            
        
        # Agora vamos entrar no laco e ler do host local
        # enviar para o host remoto enviar para o host local
        # enxaguar, lavar e repetir
        while True:
            
            # Le do host local
            local_buffer = receive_from(client_socket)
            
            
            
            if len(local_buffer):
                
                print "[<==] Received %d bytes from localhost." % len(local_buffer)
                hexdump(local_buffer)
                
                # Envia os dados para nosso handler de solicitacoes
                local_buffer = request_handler(local_buffer)
                
               # Envia os dados ao host remoto
                remote_socket.send(local_buffer)
                print "[==>] Sent to remote."
                
                
            # Recebe a resposta
            remote_buffer = receive_from(remote_socket)
            
            if len(remote_buffer):
                print "[<==] Received %d bytes from remote." % len(remote_buffer)
                hexdump(remote_buffer) 
                
                
                # Envia dados ao nosso handler de resposta
                remote_buffer = response_handler(remote_buffer)
		
		client_socket.send(remote_buffer)
                
                print "[==>] Sent to localhost."
            
            # Se nao houver mais dados em nenhum dos lados encerra as conexoes
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                
                print "[*] No more data. Closing connections."
                
                
                break
    

# Esta e uma  boa funcao de dumping de valores hexa diretamente obtida dos
# comentarios em:
# http://code.activete.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    
    
    
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b' '.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa,text))
        
    print b'\n'.join(result)
    
    
    
def receive_from(connection):
    buffer = ""
    # Definimos um timeout de 2 segundos; de acordo com
    # seu alvo, pode ser que esse valor precise ser ajustado
    connection.settimeout(2)
        
    try:
            # Continua lendo em buffer ate
            # que nao haja mais dados
            # ou a temporizacao    
            while True:
                data = connection.recv(4096)
                
                if not data:
                    break
                
                
                buffer += data
                
    except:
	pass
        
        
    return buffer
    
# Modifica qualquer solicitacao destinada ao host remoto
def request_handler(buffer):
    # Faz modificacoes no pacote
    return buffer


# Modifica qualquer resposta destinada ao host local
def response_handler(buffer):
    # Faz modificacoes no pacote
    return buffer


def main():
    # Sem parsing sofisticado de linha de comando nesse caso
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)
    
    # Define paramentros para ouvir localmente
    local_host  = sys.argv[1]
    local_port  = int(sys.argv[2])
    
    # Define o alvo remoto
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    # O codigo a seguir diz ao nosso proxy para conectar e receber dados
    # antes de enviar ao host remoto
    receive_first = sys.argv[5]
    
    if "True" in receive_first:
	    receive_first = True
    else:
	    receive_first = False
	    
    
    # Agora coloca em acao o nosso socket que ficara ouvindo
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)
    
    
main()