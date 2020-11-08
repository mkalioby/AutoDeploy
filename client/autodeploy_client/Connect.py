import socket, time
from . import Config
EOM = "\n\n###"


def Send(message,server,port):
    if waitTillAlive(server, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, port))
        output = str(message) + str(EOM)
        client.sendall(output.encode('utf-8'))
        chunks = []
        while True:
            buf = (client.recv(10000)).decode("utf-8")
            if len(buf) < 5:
                if len(chunks) == 0:
                    chunks.append(buf)
                else:
                    chunks[-1] += buf
            else:
                chunks.append(str(buf))
            if EOM in chunks[-1]:
                res = "".join(chunks)[:-5]
                break
        return res
    else:
        return "ERR: Cannot connect to server"


def connect(domain,port,timeout=10):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((domain, port))
        output = 'TEST: HELLO\n\n###'
        client.sendall(output.encode('utf-8'))
        client.close()
        return True
    except IOError:
        return False


def waitTillAlive(domain, port):
    for i in range(0,int(Config.failure_try)):
        if connect(domain, port):
            print("Connected To:", domain)
            return True
        else:
            time.sleep(int(Config.sleep_time))
            print("Trying again....")
    else:
        return False
