from . import Config
from . import ClientJob as Job
from . import Connect
import simplejson
import xml.dom.minidom
from operator import itemgetter
import datetime

class Client:
    scm = ""
    options = None
    msg = ""
    server =""
    port = ""
    sshkey=""

    def __init__(self, scm, server, port,key=""):
        self.scm = scm
        self.server = server
        self.port = port
        self.sshkey=key


    def _send(self, msg):
        return Connect.Send(msg, self.server, self.port)

    def Clone(self, repo, workdir, owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createCloneMessage(owner, repo, workdir, self.sshkey, self.scm, options=self.options)
        result = self._send(msg)
        return result

    def Pull(self, repo, workdir, key, owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createPullMessage(owner, workdir, self.sshkey, self.scm, options=self.options)
        result = self._send(msg)
        return result

    def ListTags(self, workdir, owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createListTagsMessage(workdir=workdir, scm=self.scm, key=self.sshkey, owner=owner)
        result = self._send(msg)
        if result == "Done": return []
        #print result
        res=[]
        for line in result.split("\n"):
            if line=="": continue
            info=line.split(",,")
            Date=datetime.datetime.strptime(info[2][:-6],"%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d %H:%M:%S")
            res.append({"Tag":info[0],"Tagger":info[1],"Date":Date,"Commit":info[3]})
        if len(res)>0:
            newlist = sorted(res, key=itemgetter('Date'), reverse=True)
            return newlist
        else:
            return []
    def ListBranchs(self,workdir,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createGetBranchs(workdir=workdir, scm=self.scm, owner=owner)
        result = self._send(msg)
        return result.split("\n")
    def SwitchTag(self, workdir, tag, owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createSwitchTagMessage(workdir=workdir, tag=tag, scm=self.scm, owner=owner)
        result = self._send(msg)
        return result

    def Deploy(self, workdir, configFile, owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createDeployMessage(workdir=workdir, configFile=configFile, scm=self.scm, owner=owner)
        result = self._send(msg)
        return result

    def Integrate(self,jobID, workdir, configFile, owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createIntegrateMessage(jobID=jobID,workdir=workdir, configFile=str(configFile), scm=self.scm, owner=owner)
        result = self._send(msg)
        return result

    def CheckUp(self):
        return Connect.connect(self.server, self.port, 5)

    def ListCommits(self, workdir, page=0, rpp=10, owner='',options=None):
        if owner == '':
            owner = Config.Owner
        msg = Job.createListCommitsMessage(workdir=workdir, scm=self.scm, owner=owner,key=self.sshkey,options=options)
        res = self._send(msg)
        result = []
        #HEAD = True
        for line in res.split("\n"):
            if "ERR:" in line: return line
            if line=="": continue
            info = line.split(",,")
            try:
                d = {"Hash": info[0], "Short": info[1], "Author": info[2], "Committed": info[3], "Message": info[4]}
                result.append(d)
            except:
                print("Error while parsing line (%s)"%line)
        return result

    def SwitchCommit(self, workdir, commit, owner=''):
        if owner == '':
            owner = Config.Owner
        msg = Job.createSwitchCommitMessage(owner, workdir, commit, self.scm)
        res = self._send(msg)
        return res

    def getCommitsDiff(self,workdir,commit,owner=''):
        if owner == '':
            owner = Config.Owner
        msg = Job.creategetCommitsDiffMessage(owner, workdir, commit, self.scm)
        res = self._send(msg)
        result=[]
        for item in res.split("\n"):
            if item=="" or item=="Done" : continue
            result.append(item)
        return result

    def getChangeLog(self, workdir, since,to, owner=''):
        if owner == '':
            owner = Config.Owner
        msg = Job.createGetChangeLog(owner, workdir,  self.scm,options={"since":since,"to":to})
        res = self._send(msg)
        result = []
        for item in res.split("\n"):
            if item == "" or item == "Done": continue
            result.append(item)
        return result