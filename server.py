#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver


def registerUser(stringInfo, usersDict, handler):

    addrStart = stringInfo[1].find(":") + 1
    usersDict[stringInfo[1][addrStart:]] = handler.client_address
    print("client", stringInfo[1][addrStart:], "registered")


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    usersDict = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """

        # print("Incoming client message from: ")
        # print(self.client_address)
        stringMsg = self.rfile.read().decode('utf-8')
        # print("Client sent: ", stringMsg)
        stringInfo = stringMsg.split(" ")
        try:
            if stringInfo[0] == 'REGISTER':
                registerUser(stringInfo, SIPRegisterHandler.usersDict, self)
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
        except:
                self.wfile.write(b"SIP/2.0 500 Server Internal Error\r\n\r\n")


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', 6001), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
