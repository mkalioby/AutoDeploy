#!/usr/bin/python3.7
from Crypto.PublicKey import RSA
import socket
import threading
import base64
import config
import Response
import Request
import Common
from scm import Git as git
from deployer import autodeployer
from integrator import autointegrator
import traceback
import yaml
JOBS = {}
EOM = Common.EOM
debug = False

def startServer():
    port = int(config.port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print("Server started at " + str(port))
    return s


def importKey():
    file = open(config.publicKey, 'r')
    st = "".join(file.readlines())
    key = RSA.importKey(st)
    return key


def validReq(req):
    key = importKey()
    x=base64.decodebytes(req["sec"].encode('utf-8'))
    decrypted = (key.decrypt(x)).decode('utf-8')
    if (req["Owner"]+req["scm"]+req["requestType"] == decrypted):
        return True
    else:
        return False


def HandleClient(clientsock):
    import config
    name = threading.currentThread().getName()
    print(name, ' Started.............')
    global EOM
    chunks = []
    cmd=""
    while 1:
        buf = clientsock.recv(2048)
        if len(buf)<6:
            chunks[-1]+=(buf).decode("utf-8")
        else:
            chunks.append((buf).decode("utf-8"))
        if (EOM in chunks[-1]):
            msg = "".join(chunks)[:-5]
            if debug:
                print(msg)
                # print("No Action")
                # return
            if (msg == "TEST: HELLO"):
                Response.sendData(clientsock,"Hello")
                clientsock.close()
                return
            req = Request.parseRequest(msg)
            if (not validReq(req)):
                Response.sendData(clientsock, "Invalid Request")
                print("invalid request")
                clientsock.close()
                return
            if (req["requestType"]=="CLONE"):
                job = Request.parseCloneJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(job["workdir"],job["repo"])
                    gclient.setKey(job["key"])
                    cmd=gclient.get_clone_cmd()
            elif (req["requestType"] == "PULL"):
                job = Request.parsePullJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    gclient.setKey(job["key"])
                    cmd=gclient.get_pull_cmd()
            elif req["requestType"]=="LIST-TAGS":
                job = Request.parseListTagsJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    gclient.setKey(job["key"])
                    cmd=gclient.get_list_tags_cmd()
                    result=[]
                    res=Common.run(cmd).decode("utf-8")
                    if "ERR:" in res:
                        Response.sendData(clientsock,res)
                    else:
                        for line in res.split("\n"):
                            try:
                                cmd="cd %s; git show %s"%(job["workdir"],line)
                                res=Common.run(cmd)
                                lines=res.split("diff --git ")[0]
                                info=lines.split("\n")
                                #print info
                                tag=info[0][4:]
                                tagger=info[1].split(": ")[1].split("<")[0].strip()
                                date=info[2].split(": ")[1].strip()
                                commit=info[6].split("commit ")[1]
                                result.append(",,".join([tag,tagger,date,commit]))
                            except:
                                pass
                        Response.sendData(clientsock,"\n".join(result))
                        return
            elif req["requestType"] == "LIST-BRNACHS":
                job = Request.parseListBranchsJob(msg)
                if job["scm"] == "git":
                    gclient = git.GIT(workdir=job["workdir"])
                    cmd = gclient.get_list_branches()
                    result = []
                    res = Common.run(cmd).decode("utf-8")
                    if "ERR:" in res:
                        Response.sendData(clientsock, res)
                    else:
                        for line in res.split("\n"):
                            try:
                                if line!="":
                                    result.append(line.replace("*","").strip())
                            except:
                                pass
                        #print result
                        Response.sendData(clientsock, "\n".join(result))
                        return
            elif req["requestType"]=="LIST-COMMITS":
                job = Request.parseGetCommitsJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    gclient.setKey(job["key"])
                    cmd=gclient.get_history_cmd(job["options"],limit=config.log_limit)
            elif req["requestType"]=="SWITCH-TAG":
                job = Request.parseSwitchTagJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    cmd=gclient.get_switch_to_tag_cmd(tag=job["tag"])
            elif req["requestType"]=="SWITCH-COMMIT":
                job = Request.parseSwitchCommitJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    cmd=gclient.switch_to_histroy_cmd(commit=job["commit"])
            elif req["requestType"]=="DIFF-COMMIT":
                job = Request.parseSwitchCommitJob(msg)
                if job["scm"]=="git":
                    gclient=git.GIT(workdir=job["workdir"])
                    cmd=gclient.commit_diff_cmd(commit=job["commit"])

            elif req["requestType"]=="LIST-CHANGES":
                job = Request.parseGetChangeLog(msg)
                if job["scm"] == "git":
                    gclient = git.GIT(workdir=job["workdir"])
                    cmd = gclient.get_changelog(since=job["options"]["since"], to=job["options"]["to"])
                    result = []
                    res = Common.run(cmd).decode("utf-8")
                    if "ERR:" in res:
                        Response.sendData(clientsock, res)
                    else:
                        for line in res.split("\n"):
                            try:
                                if line != "":
                                    result.append(line.replace("*", "").strip())
                            except:
                                pass
                        print(result)
                        Response.sendData(clientsock, "\n".join(result))
            elif req["requestType"]=="DEPLOY":
                print(msg)
                job = Request.parseDeployJob(msg)
                try:
                    config=yaml.safe_load(open(job["configFile"]))
                    autodeployer.deploy(config,job["workdir"])
                    res="Done"
                except Exception as e:
                    res="ERR:"+traceback.format_exc()
            elif req["requestType"]=="INTEGRATE":
                print(msg)
                job = Request.parseIntegrateJob(msg)
                try:
                    config=yaml.safe_load(open(job["configFile"]))
                    Response.sendData(clientsock, "Queued")
                    autointegrator.runTest(config,job["workdir"],jobID=job['jobID'])
                    res = "Done"
                except Exception as e:
                    res="ERR:"+traceback.format_exc()
            if cmd!="":
                if "ERR:" in str(cmd):
                    Response.sendData(clientsock, cmd)
                    return
                res=Common.run(cmd)

            Response.sendData(clientsock,res)
            if debug:
                print("Ended,",res)
            else:
                print("Ended")
            clientsock.close()

            break
import os
if not os.geteuid()==0:
    print("The user should be a root.")
    exit(-6)
f=open('/var/run/autodeploy-server', "w")
f.write(str(os.getpid()))
f.close()
import  sys
if "--debug" in sys.argv:  debug=True
s = startServer()
i = 0
while 1:
    clientsock, clientaddr = s.accept()
    i += 1
    print('Got connection from ', clientsock.getpeername())
    t = threading.Thread(target=HandleClient, args=[clientsock], name="Thread #" + str(i))
    t.start()

exit(0)
