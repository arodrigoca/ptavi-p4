#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import json
import time
import sched


def register2json(usersDict):

    fileName = "registered.json"
    with open(fileName, "w+") as f:
        json.dump(usersDict, f, sort_keys=True, indent=4)


def schedDelete(usersDict, user):

    # del usersDict[user]
    # register2json(usersDict)
    print("hola")


def registerUser(stringInfo, usersDict, handler):

    s = sched.scheduler(time.time, time.sleep)
    addrStart = stringInfo[1].find(":") + 1
    user = stringInfo[1][addrStart:]
    expire_time = time.strftime('%Y-%m-%d %H:%M:%S',
        time.gmtime(time.time() + int(stringInfo[3])))

    tagsDictionary = {"address": handler.client_address,
        "expires": expire_time}

    usersDict[user] = tagsDictionary
    if expire_time == 0:
        del usersDict[user]
        print("User", user, "deleted")
    else:
        s.enter(int(stringInfo[3]), 1, schedDelete(usersDict, user))
        print("client", user, "registered")

    print(usersDict)
    register2json(usersDict)


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
        except Exception as e:
                self.wfile.write(b"SIP/2.0 500 Server Internal Error\r\n\r\n")
                print("Server error:", e)


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', 6001), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
