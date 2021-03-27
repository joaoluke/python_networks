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


def run_command(command):
    # execute o comando shell ou o arquivo recebido do cliente.
    # : comando param:
    # : return: output: resultado do comando shell.
    
    # trim the newline.(delete the characters of the string end.)
    command = command.rstrip()

    # run the command and get the output back
    try:
        # run command with arguments and return its output.
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        logging.debug(output)
    except Exception as e:
        logging.error(e)
        output = b"Failed to execute command.\r\n"

    # send the output back to the client
    return output


def client_handler(client_socket):
    """
    the thread function of handling the client. 
    :param client_socket: 
    :return: 
    """
    global upload
    global execute
    global command

    # upload file
    if len(upload_destination):
        # read in all of the bytes and write to our destination
        file_buffer = ""
        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)
            file_buffer += data.decode("utf-8")
            logging.debug(data)

            # "#EOF#" tell the server, file is end.
            if "#EOF#" in file_buffer:
                file_buffer = file_buffer[:-6]
                break
            # for interaciton, like heart packet.
            client_socket.send(b"#")

        # now we take these bytes and try to write them out
        try:
            with open(upload_destination, "wb") as fw:
                fw.write(file_buffer.encode("utf-8"))
            client_socket.send(b"save file successed.\n")
        except Exception as err:
            logging.error(err)
            client_socket.send(b"save file failed.\n")
        finally:
            client_socket.close()

    # execute the given file
    if len(execute):
        # run the command
        output = run_command(execute)

        client_socket.send(output)

    # now we go into another loop if a command shell was requested
    if command:
        # receive command from client, execute it, and send the result data.
        try:
            while True:
                # show a simple prompt
                client_socket.send(b"<BHP:#>")
                # now we receive until we see a linefeed (enter key)
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    try:
                        cmd_buffer += client_socket.recv(1024).decode("utf-8")
                    except Exception as err:
                        logging.error(err)
                        client_socket.close()
                        break
                # we have a valid command so execute it and send back the results
                response = run_command(cmd_buffer)
                # send back the response
                client_socket.send(response)
        except Exception as err:
            logging.error(err)
            client_socket.close()


def server_loop():
    """
    the server listen. create a thread to handle client's connection.
    :return: 
    """
    global target
    global port

    # if no target is defined we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    logging.info("Listen    %s:%d" % (target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


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
