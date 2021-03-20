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

# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def run_command(command):
    """
    execute the shell command, or file received from client.
    :param command: 
    :return: output: shell command result. 
    """
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
    """
    the client send datas to the server, and receive datas from server.
    :param buffer: datas from the stdin
    :return: 
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # conncet to target
        client.connect((target, port))
        logging.debug('server is %s:%d' % (target, port))

        # if we detect input from stdin then send the datas.
        # if not we are going to wait for the user to input.
        if len(buffer):
            # send the datas with utf-8 endecode.
            client.send(buffer.encode("utf-8"))

        while True:
            # now wait for datas back
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

            # wait for more input
            # Python2 is raw_input(), and Python3 is input()
            buffer = input("")
            buffer += "\n"

            client.send(buffer.encode("utf-8"))
            # logging.info("send datas: %s" % buffer)

    except Exception as e:
        logging.error(e)

    finally:
        # teardown the connection
        client.close()


def usage():
    """
    print the info of help
    :return: 
    """
    print("Usage: netcat.py -t target_host -p port")
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
    """
    parse shell option and parameters, and set the vars.
    call listen function or connect function.
    :return: 
    """
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
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

    # are we going to listen or just send data from stdin
    if not listen and len(target) and port > 0:
        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input to stdin
        # Windows is Ctrl-Z
        # buffer = sys.stdin.read()
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    # we are going to listen and potentially
    # upload things, execute commands and drop a shell back
    # depending on our command line options above
    if listen:
        server_loop()


main()
