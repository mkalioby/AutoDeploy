#! /usr/bin/python
__author__ = 'mohamed'

import os,django,django.utils.timezone as timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoDeploy.settings")
django.setup()

def savePID():
    f=open('/var/run/autodeploy-check', "w")
    f.write(str(os.getpid()))
    f.close()

def getPreviousPID():
    if not os.path.exists("/var/run/autodeploy-check"): return 0
    f=open('/var/run/autodeploy-check', "r")
    return int(f.read().strip())

def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

from autodeploy.models import *
from autodeploy_client import Client

pid=getPreviousPID()
if pid!=0:
    if check_pid(pid):
        print "Another check is running, exiting...."
        exit(-13)
savePID()


def deploy(project,server,dep_type,version):
    D= Deployment_Server()
    c = Client(str(project.repo_type), server.ip, server.port)
    D.project = project
    D.server = server
    if dep_type=="tag":
        res = c.SwitchTag(project.working_dir, version)
        D.update_type="tag"
        D.update_version=version
        project.lastTag=version
    elif dep_type=="commit" :
        if version != "HEAD":
            res=c.SwitchCommit(project.working_dir,version)
        D.update_type="commit"
        D.update_version = version
        project.lastCommit=version
    res = c.Deploy(project.working_dir, project.configFile)
    if not "ERR:" in res:
        D.datetime=timezone.now()
        D.has_new_version=False
        D.save()
        project.lastUpdate=timezone.now()
        project.newVersion=False
        project.save()
        print project.deployment_link
        if not "http://" in project.deployment_link:
            print "in if"
            link="http://"+server.DNS+project.deployment_link
            print link
            if project.emailUsers!="" or project.emailUsers!=" ":
               try:
                    Common.send(project.emailUsers.replace(",",";"),"New version of %s deployed"%project.name,"Dear User,<br/> This is an automated notification that a new version of %s has been deployed at: %s"%(project.name,link),fromUser=None,cc="",bcc="",)
                except:
                    pass
            return res+",,"+link
        else:
            print "in else"
            link=project.deployment_link
            if project.emailUsers!="" or project.emailUsers!=" ":
                try:
                    Common.send(project.emailUsers.replace(",",";"),"New version of %s deployed"%project.name,"Dear User,<br/> This is an automated notification that a new version of %s has been deployed at: %s"%(project.name,link),fromUser=None,cc="",bcc="",)
                except:
                    pass
            return res+",,"+link
    else:
        return res



for project in Project.objects.all():
    updateRequired=False
    print "Checking %s on %s"%(project.name,project.default_server.DNS)
    c=Client(str(project.repo_type),project.default_server.ip,project.default_server.port,project.sshKey.key)
    c.Pull(project.repo,project.working_dir,project.sshKey.key)
    if project.update_style=="commit":
        commits=c.ListCommits(project.working_dir)
        if  project.lastCommit != commits[0]["Hash"]:
            updateRequired=True
        if project.autoDeploy:
            deploy(project,project.default_server,"commit",commits[0]["Hash"])


    else:
        tags = c.ListTags(project.working_dir)
        if len(tags)>0:
            if project.lastTag != tags[0]["Tag"]:
                updateRequired=True
                if project.autoDeploy:
                    deploy(project,project.default_server,"tag",tags[0]["Tag"])
        else:
            print "No Tags Found"

    if updateRequired:
        project.newVersion=True

        project.save()
        print "Update Required"
    else:
        print "Already up-to-date."