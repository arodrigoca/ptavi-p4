#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    usersList = []

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """

        print("Incoming client message from: ")
        print(self.client_address)
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        for line in self.rfile:
            stringMsg = line.decode('utf-8')
            print("Client sent: ", stringMsg)
            addrIndx = stringMsg.find(":")
            break

if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', 6001), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
