import socket, base64, time, sys, subprocess
from . import Config

EOM = "\n\n###"


def Send(message,server,port):
    if waitTillAlive(server, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, port))
        client.send(message + EOM)
        chunks = []
        while True:
            buf = client.recv(10000)
            if len(buf) < 5:
                chunks[-1] += buf
            else:
                chunks.append(str(buf))
            if EOM in chunks[-1]:
                res = "".join(chunks)[:-5]
                break
        return res


def connect(domain,port,timeout=10):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((domain, port))
        client.send("TEST: HELLO\n\n###")
        client.close()
        return True
    except IOError:
        return False


def waitTillAlive(domain, port):
    secondTime = False
    while (1):
            if connect(domain,port):
                if secondTime: print("Connected To:",domain)
                break
            else:
                time.sleep(5)
                secondTime = True
                print("Trying again....")
    return True

