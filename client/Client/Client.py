import Config
import ClientJob as Job
import Connect
import simplejson
import xml.dom.minidom


class Client:
    scm = ""
    options = None
    msg = ""
    server=Config.ServerHost
    port=Config.ServerPort
    def __init__(self, scm,server,port):
        self.scm = scm
        self.server= server
        self.port= port
    def _send(self, msg):
        return self._send(msg,self.server,self.port)

    def Clone(self, repo, workdir, key, server, port, owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createCloneMessage(owner, repo, workdir, key, self.scm, options=self.options)
        result = self._send(msg)
        return result

    def Pull(self, repo,workdir,key,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createPullMessage(owner, workdir, self.scm, options=self.options)
        result = self._send(msg)
        return result

    def ListTags(self,workdir,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg=Job.createListTagsMessage(workdir=workdir,scm=self.scm,owner=owner)
        result = self._send(msg)
        return result

    def SwitchTag(self,workdir,tag,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg=Job.createSwitchTagMessage(workdir=workdir,tag=tag,scm=self.scm,owner=owner)
        result = self._send(msg)
        return result

    def Deploy(self,workdir, configFile,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg=Job.createDeployMessage(workdir=workdir,configFile=configFile,scm=self.scm,owner=owner)
        result = self._send(msg)
        return result

    def CheckUp(self):
        return Connect.connect(self.server,self.port,5)


