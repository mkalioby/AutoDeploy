#!/usr/bin/python
from Crypto.PublicKey import RSA
import socket
import threading
import base64
import config
import Response
import Request
import Common


JOBS = {}
EOM = Common.EOM


def startServer():
    port = int(config.port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print "Server started at " + str(port)
    return s


def importKey():
    file = open(config.publicKey, 'r')
    st = "".join(file.readlines())
    key = RSA.importKey(st)
    return key


def validReq(req):
    key = importKey()
    decrypted = key.decrypt(base64.decodestring(req["sec"]))
    if (req["JobID"] + req["Owner"] == decrypted):
        return True
    else:
        return False


def HandleClient(clientsock):
    name = threading.currentThread().getName()
    print name, ' Started.............'
    global EOM
    chunks = []
    while 1:
        buf = clientsock.recv(2048)
        chunks.append(str(buf))
        if (EOM in chunks[-1]):
            msg = "".join(chunks)[:-5]
            if (msg == "TEST: HELLO"):
                return
            req = Request.parseRequest(msg)
            if (not validReq(req)):
                Response.sendData(clientsock, "Invalid Request")
                print "invalid request"
                clientsock.close()
                return
            if (req["requestType"] == "SUBMIT"):
                job = Request.parseJob(msg)
                global JOBS
                if (req["Owner"] == "system" or req["Owner"] == "utils"):
                    res = Common.run(job["command"], req["JobID"])
                    if req["Owner"] == "system":
                        Response.sendData(clientsock, "Done")
                    else:
                        Response.sendData(clientsock, res)
                clientsock.close()

            break


s = startServer()
i = 0
while 1:
    clientsock, clientaddr = s.accept()
    i += 1
    print 'Got connection from ', clientsock.getpeername()
    t = threading.Thread(target=HandleClient, args=[clientsock], name="Thread #" + str(i))
    t.start()

exit(0)
