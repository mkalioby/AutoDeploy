import socket, time
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
