#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import json
import time
import sched
import _thread

scheduler = sched.scheduler(time.time, time.sleep)


def deleteUser(usersDict, user):

    try:
        del usersDict[user]
        print("User", user, "deleted", "because its entry expired")
        SIPRegisterHandler.register2json(usersDict)

    except KeyError:
        print("No entry for", user)


def schedDelete(usersDict, user):

    try:
        scheduler.enterabs(usersDict[user]["fromEpoch"], 1, deleteUser,
                           (usersDict, user))
        scheduler.run()
    except KeyError:
        pass


def registerUser(stringInfo, usersDict, handler):

    addrStart = stringInfo[1].find(":") + 1
    user = stringInfo[1][addrStart:]
    expire_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                time.gmtime(time.time() + int(stringInfo[3])))

    tagsDictionary = {"address": handler.client_address,
                      "expires": expire_time,
                      "fromEpoch": time.time() + int(stringInfo[3])}

    usersDict[user] = tagsDictionary
    if int(stringInfo[3]) == 0:
        deleteUser(usersDict, user)
    else:
        print("client", user, "registered", "for",
              int(stringInfo[3]), "seconds")

    _thread.start_new_thread(schedDelete, (usersDict, user))
    SIPRegisterHandler.register2json(usersDict)


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

        stringMsg = self.rfile.read().decode('utf-8')
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

    @classmethod
    def register2json(self, usersDict):

        fileName = "registered.json"
        with open(fileName, "w+") as f:
            json.dump(usersDict, f, sort_keys=True, indent=4)

    @classmethod
    def json2registered(self):

        try:
            with open("registered.json", "r+") as f:
                print("Reading json file")
                initDict = json.load(f)
                self.usersDict = initDict
                for user in self.usersDict:
                    _thread.start_new_thread(schedDelete,
                                             (self.usersDict, user))
        except FileNotFoundError:
            print("json file not found")


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', 6001), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        SIPRegisterHandler.json2registered()
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
