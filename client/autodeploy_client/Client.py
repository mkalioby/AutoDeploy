import Config
import ClientJob as Job
import Connect
import simplejson
import xml.dom.minidom


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
        msg = Job.createCloneMessage(owner, repo, workdir, aself.sshkey, self.scm, options=self.options)
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

    def CheckUp(self):
        return Connect.connect(self.server, self.port, 5)

    def ListCommits(self, workdir, page=0, rpp=10, owner=''):
        if owner == '':
            owner = Config.Owner
        msg = Job.createListCommitsMessage(workdir=workdir, scm=self.scm, owner=owner,key=self.sshkey)
        res = self._send(msg)
        result = []
        #HEAD = True
        for line in res.split("\n")[1:]:
            info = line.split(",,")
            # print line
         #   if HEAD:
          #      info[0] = "HEAD"
           #     HEAD = False
            try:
                d = {"Hash": info[0], "Short": info[1], "Author": info[2], "Committed": info[3], "Message": info[4]}
                result.append(d)
            except:
                print "Error while parsing line (%s)"%line
        print result
        return result

    def SwitchCommit(self, workdir, commit, owner=''):
        if owner == '':
            owner = Config.Owner
        msg = Job.createSwitchCommitMessage(owner, workdir, commit, self.scm)
        res = self._send(msg)
        return res