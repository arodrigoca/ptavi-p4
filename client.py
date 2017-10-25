#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

def sendRegister(server, port, sipmsg, my_socket, myaddr):

    finalMsg = sipmsg + " " + "sip:" + myaddr + " " + "SIP/2.0\r\n\r\n"
    # print("Enviando:", finalMsg)
    my_socket.send(bytes(finalMsg, 'utf-8'))
    data = my_socket.recv(1024)
    print()
    print('Received:', data.decode('utf-8'))


def doClient(server, port, sipmsg, myaddr):

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        try:
            my_socket.connect((server, port))

        except socket.gaierror:
            sys.exit('Incorrect or not found server tuple')

        sendRegister(server, port, sipmsg, my_socket, myaddr)
    print("Socket terminado.")


if __name__ == "__main__":
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    try:
        SERVER = sys.argv[1]
        PORT = int(sys.argv[2])
        SIPMSG = sys.argv[3]
        SIPMSG = SIPMSG.upper()
        MYADDR = ' '.join(sys.argv[4:])

    except(FileNotFoundError, IndexError):
        sys.exit('Usage: IP_ADDRESS PORT, STRING')

    doClient(SERVER, PORT, SIPMSG, MYADDR)
