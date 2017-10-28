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
import threading

scheduler = sched.scheduler(time.time, time.sleep)


def register2json(usersDict):

    fileName = "registered.json"
    with open(fileName, "w+") as f:
        json.dump(usersDict, f, sort_keys=True, indent=4)


def json2registered(SIPHandler):

    try:
        with open("registered.json", "r+") as f:
            initDict = json.load(f)
            SIPHandler.usersDict = initDict
            for user in SIPHandler.usersDict:
                _thread.start_new_thread(schedDelete, (SIPHandler.usersDict, user, SIPHandler.usersDict[user]["timeout"]))
    except FileNotFoundError:
            print("json file not found")


def deleteUser(usersDict, user):

    try:
        del usersDict[user]
        print("User", user, "deleted")
        register2json(usersDict)

    except KeyError:
        print("No entry for", user)

def schedDelete(usersDict, user, delay):

    scheduler.enterabs(time.time() + delay, 1, deleteUser, (usersDict, user))
    scheduler.run()


def registerUser(stringInfo, usersDict, handler):

    addrStart = stringInfo[1].find(":") + 1
    user = stringInfo[1][addrStart:]
    expire_time = time.strftime('%Y-%m-%d %H:%M:%S',
        time.gmtime(time.time() + int(stringInfo[3])))

    tagsDictionary = {"address": handler.client_address,
        "expires": expire_time, "timeout": int(stringInfo[3])}

    usersDict[user] = tagsDictionary
    if int(stringInfo[3]) == 0:
        deleteUser(usersDict, user)
    else:
        print("client", user, "registered")

    _thread.start_new_thread(schedDelete, (usersDict, user, int(stringInfo[3])))
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
        json2registered(SIPRegisterHandler)
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
