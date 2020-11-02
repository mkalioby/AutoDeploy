__author__ = 'mohamed'

import deployment.models as CDModels
import integration.models as CIModels
from . import Common
import simplejson
import sys
sys.path.append("../../../client")
from autodeploy_client.Client import Client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.utils import timezone
from jose import jwt
from slacker import Slacker


def checkServers(request):
    res = {}
    for server in CDModels.Server.objects.all():
        c = Client("git", server.ip, server.port)
        state = c.CheckUp()
        if state:
            res[server.name] = "UP"
        else:
            res[server.name] = "DOWN"
    return HttpResponse(simplejson.dumps(res))


@csrf_protect
def cloneCD(request):
    scm = str(request.GET["scm"])
    ip = str(request.GET["ip"])
    port = int(request.GET["port"])
    project = CDModels.Project.objects.get(name=request.GET["project_name"])
    c = Client(scm, ip, port, project.sshKey.key)
    res = c.Clone(project.repo, project.working_dir)
    if res == '': res = 'Done'
    return HttpResponse(res)

@csrf_protect
def cloneCI(request):
    scm = str(request.GET["scm"])
    ip = str(request.GET["ip"])
    port = int(request.GET["port"])
    project = CIModels.CIProject.objects.get(name=request.GET["project_name"])
    c = Client(scm, ip, port, project.sshKey.key)
    res = c.Clone(project.repo, project.working_dir)
    if res == '': res = 'Done'
    return HttpResponse(res)


@csrf_protect
def deploy(request):
    server = CDModels.Server.objects.get(name=request.session["deploy_server"])
    project = CDModels.Project.objects.get(name=request.session["deploy_project"])
    last_Deployment = None
    try:
        last_Deployment = CDModels.Deployment_Server.objects.filter(server=server, project=project).latest()
    except:
        pass
    D = CDModels.Deployment_Server()
    c = Client(str(project.repo_type), server.ip, server.port)
    D.project = project
    D.server = server
    if "tag" in request.GET:
        res = c.SwitchTag(project.working_dir, request.GET["tag"])
        D.update_type = "tag"
        D.update_version = request.GET["tag"]
        project.lastTag = request.GET["tag"]
    elif "commit" in request.GET:
        if request.GET["commit"] != "HEAD":
            res = c.SwitchCommit(project.working_dir, request.GET["commit"])
        D.update_type = "commit"
        D.update_version = request.GET["commit"]
        project.lastCommit = request.GET["commit"]
    res = c.Deploy(project.working_dir, project.configFile)
    if not "ERR:" in res:
        D.datetime = timezone.now()
        D.has_new_version = False
        D.save()
        project.lastUpdate = timezone.now()
        project.newVersion = False
        project.save()
        print(project.deployment_link)
        if not "http://" in project.deployment_link:
            print("in if")
            link = "http://" + server.DNS + project.deployment_link
            print(link)
            if project.emailUsers != "" or project.emailUsers != " " and last_Deployment != None:
                changes = c.getChangeLog(project.working_dir, since=last_Deployment.update_version,
                                         to=request.GET["commit"])
                changes_text = "<h3>Changes</h3><ul>"
                found = False
                for change in changes:
                    if change.endswith(":"): continue
                    changes_text += "<li>%s</li>" % change
                    found = True
                if found:
                    changes_text += "</ul>"
                else:
                    changes_text = ""
                Common.send(project.emailUsers.replace(",", ";"), "New version of %s deployed" % project.name,
                            "Dear User,<br/> This is an automated notification that a new version of %s has been deployed at: %s<br/>%s" % (
                            project.name, link, changes_text), fromUser=None, cc="", bcc="", )

            return HttpResponse(res + ",," + link)
        else:
            print("in else")
            link = project.deployment_link
            if project.emailUsers != "" or project.emailUsers != " ":
                changes = c.getChangeLog(project.working_dir, since=last_Deployment.update_version,
                                         to=request.GET["commit"])
                changes_text = "<h3>Changes</h3><ul>"
                found = False
                for change in changes:
                    if change.endswith(":"): continue
                    changes_text += "<li>%s</li>" % change
                    found = True
                if found:
                    changes_text += "</ul>"
                else:
                    changes_text = ""

                Common.send(project.emailUsers.replace(",", ";"), "New version of %s deployed" % project.name,
                            "Dear User,<br/> This is an automated notification that a new version of %s has been deployed at: %s.<br>%s" % (
                            project.name, link, changes_text), fromUser=None, cc="", bcc="", )
            return HttpResponse(res + ",," + link)
    else:
        return HttpResponse(res)

@csrf_protect
def integrate(request):
    commit = request.GET.get("commit",None)
    tag = request.GET.get("tag",None)
    server = CDModels.Server.objects.get(name=request.session["integrate_server"])
    project = CIModels.CIProject.objects.get(name=request.session["integrate_project"])
    integrate_core(server,project,tag,commit)

def integrate_core(server,project,tag=None,commit=None):
    D = CIModels.Integration_server()
    c = Client(str(project.repo_type), server.ip, server.port)
    D.project = project
    D.server = server
    change_type = None
    change_id = None
    if tag:
        res = c.SwitchTag(project.working_dir, tag)
        D.update_type = "tag"
        D.update_version = tag
        project.lastTag = tag
        change_type = "tag"
        change_id = tag
    elif commit:
        D.update_type = "commit"
        D.update_version = commit
        project.lastCommit = commit
        change_type = "commit"
        change_id = commit
    project.lastUpdate = timezone.now()
    project.newVersion = False
    project.save()
    D.datetime = timezone.now()
    D.has_new_version = False
    D.save()
    res = c.Integrate(D.pk, project.working_dir,project.name,change_type,change_id,configFile=project.configFile if project.configFile else None)
    if "Queued" in res:
        D.status_id = 1  # Running
        D.save()

def decrypt_result(msg):
    from autodeploy_client.Config import privateKey
    file = open(privateKey, 'r')
    st = "".join(file.readlines())
    return jwt.decode(msg, st, "RS256")

@csrf_exempt
def receive_integrate_result(request):
    errors = {}
    if request.method == "GET":
        print("Hello This is RIS")
    else:
        result = decrypt_result(simplejson.loads(request.body))
        IS = CIModels.Integration_server.objects.get(id=result['jobID'])
        IS_output = result['output']
        success = True
        IS.author_name = IS_output['author_name']
        IS.author_email = IS_output['author_email']
        IS.branch = IS_output['branch']
        coverage = IS_output.get('Coverage', None)
        IS.coverage = coverage
        del IS_output['author_name']
        del IS_output['author_email']
        del IS_output['branch']
        if coverage or "Coverage" in IS_output.keys():
            del IS_output['Coverage']
        for k, v in IS_output.items():
            if v['exit_code'] not in [0, '0']:
                success = False
        IS.status_id = 2 if success else 3

        slack = Slacker('xoxb-1449004581684-1482854233264-jLUGzlqrs6VL8JKF9e85FARJ')
        response = slack.users.list()
        channels = slack.conversations.list().body['channels']
        users = response.body['members']
        project = CIModels.CIProject.objects.get(name=IS.project.name)
        commit_link = project.repo_link.split("src")[0] + 'commits/' + project.lastCommit
        user_id = None
        channel_id = None
        for user in users:
            if user['profile'].get('email', None) == IS.author_email:
                user_id = user['id']
        for ch in channels:
            if project.slackchannel and project.slackchannel == ch['name']:
                channel_id = ch['id']
        if user_id:
            message = "Hello <@" + user_id + "> , your last <" + commit_link + "|" + IS.update_type + "> in branch " + IS.branch + " was failed" if not success else " was success"
            slack.chat.post_message(user_id, message)
            if channel_id:
                slack.chat.post_message(channel_id, message)
        IS.result = IS_output
        IS.save()
    return HttpResponse(simplejson.dumps(errors), content_type="application/json")