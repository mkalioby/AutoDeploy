__author__ = 'mohamed'
from BaseSCM import BaseSCM
import Common

class GIT(BaseSCM):

    def __init__(self,workdir,repo=""):
        self.workdir=workdir
        self.repo=repo
    def setKey(self,key):
        from os.path import expanduser
        home = expanduser("~")
        keyfile=home+"/.ssh/id_rsa"
        Common.run("chmod 700 %s"%keyfile)
        f=open(keyfile,"w")
        f.write(key)
        f.close()
        Common.run("chmod 400 %s;ssh-add %s"%(keyfile,keyfile))
    def get_clone_cmd(self):
        return "git clone %s %s"%(self.repo,self.workdir)
    def get_pull_cmd(self):
        return "cd %s; git pull"%self.workdir
    def get_list_tags_cmd(self):
        return "cd %s;git tag -l"%self.workdir

    def get_list_branches(self):
        return "cd %s;git branch -a" % self.workdir

    def get_switch_to_tag_cmd(self,tag):
        return "cd %s; git checkout tags/%s"%(self.workdir,tag)
    def get_history_cmd(self,options={}):
        branch=options.get("branch","")
        cmd =  'cd ' + self.workdir +'; git log '
        if branch!="":
            cmd += branch
        else:
            cmd+= ' --all '
        cmd += ' --pretty=format:"%H,,%h,,%an,,%ar,,%s,,%cd"  | cat -'
        return cmd
    def switch_to_histroy_cmd(self,commit):
        return 'cd %s; git reset --hard %s'%(self.workdir,commit)
    def commit_diff_cmd(self,commit):
        Common.run(self.get_pull_cmd())
        return 'git rev-list %s..HEAD'%(commit)
