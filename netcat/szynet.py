#!/usr/bin/env python3
# -*- code: utf-8 -*-

import sys
import getopt
import socket
import subprocess
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    # datefmt='%Y/%m/%d %H:%M:%S',
                    # filename='myapp.log',
                    filemode='a')

# Define variáveis globais
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def client_handler(client_socket):
    # A função thread de lidar com o cliente.
    # :param client_socket: 
    # :return: 
    
    global upload
    global execute
    global command

    # Verifica se é upload
    if len(upload_destination):
        # Lê todos os bytes e grava em nosso destino
        file_buffer = ""
        # Permanece lendo os dados até que não haja mais nenhum disponível
        while True:
            data = client_socket.recv(1024)
            file_buffer += data.decode("utf-8")
            logging.debug(data)

            # "#EOF#" diz ao servidor que o arquivo está finalizado.
            if "#EOF#" in file_buffer:
                file_buffer = file_buffer[:-6]
                break
           
            client_socket.send(b"#")

        # Agora teremos de gravas esses byteshj vb9k
        try:
            with open(upload_destination, "wb") as fw:
                fw.write(file_buffer.encode("utf-8"))
            # Confirma que gravamos o arquivo
            client_socket.send(b"save file successed.\n")
        except Exception as err:
            logging.error(err)
            client_socket.send(b"save file failed.\n")
        finally:
            client_socket.close()

    # Verifica se é execução de comando
    if len(execute):
        # Executa o comando
        output = run_command(execute)

        client_socket.send(output)

    # Entra em outro laço se um shell de comandos foi solicitado
    if command:
        # Recebe o comando do cliente, execute-o e envie os dados do resultado.
        try:
            while True:
                # Mostra um prompt simples
                client_socket.send(b"<BHP:#>")
                # Agora ficamos recebendo dados até vermos um linefeed - (tecla ENTER)
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    try:
                        cmd_buffer += client_socket.recv(1024).decode("utf-8")
                    except Exception as err:
                        logging.error(err)
                        client_socket.close()
                        break
                # Envia de volta a saída do comando
                response = run_command(cmd_buffer)
                # Envia de volta a resposta
                client_socket.send(response)
        except Exception as err:
            logging.error(err)
            client_socket.close()


def server_loop():
    # O servidor escuta e crie um thread para lidar com a conexão do cliente.
    # :return: 
    
    global target
    global port

    # Se não houver nenhum alvo definido, ouviremos todas as interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    logging.info("Listen    %s:%d" % (target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # Dispara uma thread para cuidar do nosso novo cliente
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    # execute o comando shell ou o arquivo recebido do cliente.
    # : comando param:
    # : return: output: resultado do comando shell.
    
    # Remove a quebra de linha
    command = command.rstrip()

    # Executa o comando e obtém os dados de saída
    try:
        # Execute o comando com argumentos e retorne sua saída.
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        logging.debug(output)
    except Exception as e:
        logging.error(e)
        output = b"Failed to execute command.\r\n"

    # Envia os dados de saída de volta ao cliente
    return output

def client_sender(buffer):
    # O cliente envia dados para o servidor e recebe dados do servidor.
    # : param buffer: dados do stdin
    # : retorn:
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao nosso host-alvo
        client.connect((target, port))
        logging.debug('server is %s:%d' % (target, port))

        # Se detectarmos a entrada de stdin, enviaremos os dados.
        # Se não, vamos esperar a entrada do usuário.
        if len(buffer):
            # Agora espera receber dados de volta (encriptados).
            client.send(buffer.encode("utf-8"))

        while True:
            # Agora espere pelos dados de volta
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                logging.debug("receive datas : %s" % data)

                try:
                    response += data.decode("utf-8")
                except Exception as e:
                    logging.error(e)
                    response += data.decode("gbk")

                if recv_len < 4096:
                    break

            print(response + " ")

            # Espera mais dados de entrada
            buffer = input("")
            buffer += "\n"

            client.send(buffer.encode("utf-8"))

    except Exception as e:
        logging.error(e)

    finally:
        # Encerra a conexão
        client.close()


def usage():
    # imprima informações de ajuda
    # :return: 
    
    print("Usage: szynet.py -t target_host -p port")
    print("\t-l --listen                - listen on [host]:[port] for incoming connections")
    print("\t-e --execute=file_to_run   - execute the given file upon receiving a connection")
    print("\t-c --command               - initialize a command shell")
    print("\t-u --upload=destination    - upon receiving connection upload a file and write to [destination]")
    print("Examples: ")
    print("\tnetcat.py -t 192.168.1.3 -p 5555 -l -c")
    print("\tnetcat.py -t 192.168.1.3 -p 5555 -l -u=c:\\target.exe")
    print("\tnetcat.py -t 192.168.1.3 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("\techo 'ABCDEFGHI' | ./netcat.py.py -t192.168.1.7 -p80")
    sys.exit(0)


def main():
    # passe a opção e os parâmetros do shell e defina as variáveis.
    # chame a função de escuta ou a função de conexão.
    # :return: 
    
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # Lê as linhas de comando
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute=", "target=", "port=", "command", "upload="])
    except getopt.GetoptError as err:
        logging.error("%s", err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
            usage()

    # Iremos ouvir ou simplesmente enviar dados stdin?
    if not listen and len(target) and port > 0:
        # Lê o buffer da linha de comando
        # isso causará um bloqueio, portando envie um CTRL-D se não estiver
        # enviando dados de entrada stdin
        # Windows é Ctrl-Z
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    # Iremos ouvir a porta e, potencialmente,
    # faremos upload de dados, executaremos comandos e deixaremos um shell
    # de acordo com as opções de linha de comando anteriores
    if listen:
        server_loop()


main()
