#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys


def doClient(server, port, line):

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        try:
            my_socket.connect((server, port))

        except socket.gaierror:
            sys.exit('Incorrect or not found server tuple')

        print("Enviando:", line)
        my_socket.send(bytes(line, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))

    print("Socket terminado.")


if __name__ == "__main__":
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    try:
        SERVER = sys.argv[1]
        PORT = int(sys.argv[2])
        LINE = ' '.join(sys.argv[3:])

    except(FileNotFoundError, IndexError):
        sys.exit('Usage: IP_ADDRESS PORT, STRING')

    doClient(SERVER, PORT, LINE)
