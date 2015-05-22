#! /usr/bin/python
__author__ = 'mohamed'

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoDeploy.settings")
django.setup()

from autodeploy.models import *
from autodeploy_client import Client

for project in Project.objects.all():
    updateRequired=False
    print "Checking %s on %s"%(project.name,project.default_server.DNS)
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
            print "No Tags Found"

    if updateRequired:
        project.newVersion=True
        project.save()
        print "Update Required"
    else:
        print "Already up-to-date."