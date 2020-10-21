#! /usr/bin/python
__author__ = 'mohamed'

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoDeploy.settings")
django.setup()

autodeploy_check_path = "/home/mahmood/Work/autodeploy/autodeploy-check"


def savePID():
    f = open(autodeploy_check_path, "w")
    f.write(str(os.getpid()))
    f.close()


def getPreviousPID():
    if not os.path.exists(autodeploy_check_path): return 0
    f = open(autodeploy_check_path, "r")
    return int(f.read().strip())


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


from integration.models import CIProject
from autoDeploy.api import integrate_core
from deployment.models import Server
from autodeploy_client import Client


def send_integration_request(server, project, tag=None, commit=None):
    print("integrate_core => ",server,project,commit,tag)
    integrate_core(server, project,tag,commit)


pid = getPreviousPID()
if pid != 0:
    if check_pid(pid):
        print("Another check is running, exiting....")
        exit(-13)
savePID()

for project in CIProject.objects.all():
    updateRequired = False
    print("Checking %s on %s" % (project.name, project.default_server.DNS))
    c = Client(str(project.repo_type), project.default_server.ip, project.default_server.port, project.sshKey.key)
    c.Pull(project.repo, project.working_dir, project.sshKey.key)
    if project.update_style == "commit":
        commits = c.ListCommits(project.working_dir)
        if project.lastCommit != commits[0]["Hash"]:
            updateRequired = True
            server = Server.objects.get(name=project.default_server)
            send_integration_request(server, project, commit=commits[0]['Hash'])

    else:
        tags = c.ListTags(project.working_dir)
        if len(tags) > 0:
            if project.lastTag != tags[0]["Tag"]:
                updateRequired = True
                server = Server.objects.get(name=project.default_server)
                send_integration_request(server, project, tag=tags[0]['Tag'])
        else:
            print("No Tags Found")

    if updateRequired:
        project.newVersion = True
        project.save()
        print("Update Required")
    else:
        print("Already up-to-date.")
