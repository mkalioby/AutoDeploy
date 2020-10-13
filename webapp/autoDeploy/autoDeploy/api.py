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
    return HttpResponse(res)

@csrf_protect
def cloneCI(request):
    scm = str(request.GET["scm"])
    ip = str(request.GET["ip"])
    port = int(request.GET["port"])
    project = CIModels.CIProject.objects.get(name=request.GET["project_name"])
    c = Client(scm, ip, port, project.sshKey.key)
    res = c.Clone(project.repo, project.working_dir)
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
    if tag:
        res = c.SwitchTag(project.working_dir, tag)
        D.update_type = "tag"
        D.update_version = tag
        project.lastTag = tag
    elif commit:
        if commit != "HEAD":
            res = c.SwitchCommit(project.working_dir, commit)
        D.update_type = "commit"
        D.update_version = commit
        project.lastCommit = commit
    D.datetime = timezone.now()
    D.has_new_version = False
    D.save()
    res = c.Integrate(D.pk, project.working_dir, project.configFile)
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
        for k, v in IS_output.items():
            if v['exit_code'] not in [0, '0']:
                success = False
        IS.status_id = 2 if success else 3
        IS.result = IS_output
        IS.save()
    return HttpResponse(simplejson.dumps(errors), content_type="application/json")