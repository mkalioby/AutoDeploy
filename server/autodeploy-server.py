#!/usr/bin/python
from Crypto.PublicKey import RSA
import socket
import threading
import base64
import config
import Response
import Request
import Common
import scm.Git as git
from deployer import autodeployer
import  traceback
import yaml
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
    if (req["Owner"]+req["scm"]+req["requestType"] == decrypted):
        return True
    else:
        return False


def HandleClient(clientsock):
    name = threading.currentThread().getName()
    print name, ' Started.............'
    global EOM
    chunks = []
    cmd=""
    while 1:
        buf = clientsock.recv(2048)
        chunks.append(str(buf))
        if (EOM in chunks[-1]):
            msg = "".join(chunks)[:-5]
            print msg
            if (msg == "TEST: HELLO"):
                return
            req = Request.parseRequest(msg)
            if (not validReq(req)):
                Response.sendData(clientsock, "Invalid Request")
                print "invalid request"
                clientsock.close()
                return
            if (req["requestType"]=="CLONE"):
                job = Request.parseCloneJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(job["repo"],job["workdir"])
                    gclient.setKey(job["key"])
                    cmd=gclient.get_clone_cmd()
            elif (req["requestType"] == "PULL"):
                job = Request.parsePullJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    cmd=gclient.get_pull_cmd()
            elif req["requestType"]=="LIST-TAGS":
                job = Request.parseListTagsJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    cmd=gclient.get_list_tags_cmd()
            elif req["requestType"]=="SWITCH-TAG":
                job = Request.parseSwitchTagJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    cmd=gclient.get_switch_to_tag_cmd(tag=job["tag"])

            elif req["requestType"]=="DEPLOY":
                print msg
                job = Request.parseDeployJob(msg)
                try:
                    config=yaml.safe_load(open(job["configFile"]))
                    autodeployer.deploy(config,job["workdir"])
                    res="Done"
                except Exception as e:
                    res="ERR:"+traceback.format_exc()
            if cmd!="":
                print cmd
                res=Common.run(cmd)
            Response.sendData(clientsock,res)
            print "Ended,",res
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
