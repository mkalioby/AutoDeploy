import Config
import ClientJob as Job
import Connect
import simplejson
import xml.dom.minidom


class Client:
    scm = ""
    options = None
    msg = ""

    def __init__(self, scm):
        self.scm = scm

    def Clone(self, repo,workdir,key,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createCloneMessage(owner, repo, workdir, key, self.scm, options=self.options)
        result = Connect.Send(msg)
        return result

    def Pull(self, repo,workdir,key,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg = Job.createPullMessage(owner, workdir, self.scm, options=self.options)
        result = Connect.Send(msg)
        return result

    def ListTags(self,workdir,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg=Job.createListTagsMessage(workdir=workdir,scm=self.scm,owner=owner)
        result = Connect.Send(msg)
        return result

    def SwitchTag(self,workdir,tag,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg=Job.createSwitchTagMessage(workdir=workdir,tag=tag,scm=self.scm,owner=owner)
        result = Connect.Send(msg)
        return result

    def Deploy(self,workdir, configFile,owner=''):
        global msg
        if owner == '':
            owner = Config.Owner
        msg=Job.createDeployMessage(workdir=workdir,configFile=configFile,scm=self.scm,owner=owner)
        result = Connect.Send(msg)
        return result
