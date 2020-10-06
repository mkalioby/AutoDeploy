#! /usr/bin/python
__author__ = 'mohamed'

import os,django
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
        print("Another check is running, exiting....")
        exit(-13)
savePID()

for project in Project.objects.all():
    updateRequired=False
    print("Checking %s on %s"%(project.name,project.default_server.DNS))
    c=Client(str(project.repo_type),project.default_server.ip,project.default_server.port,project.sshKey.key)
    c.Pull(project.repo,project.working_dir,project.sshKey.key)
    if project.update_style=="commit":
        commits=c.ListCommits(project.working_dir)
        if  project.lastCommit != commits[0]["Hash"]:
            updateRequired=True

    else:
        tags = c.ListTags(project.working_dir)
        if len(tags)>0:
            if project.lastTag != tags[0]["Tag"]:
                updateRequired=True
        else:
            print("No Tags Found")

    if updateRequired:
        project.newVersion=True
        project.save()
        print("Update Required")
    else:
        print("Already up-to-date.")