__author__ = 'mohamed'
from models import *
import simplejson
from  autodeploy_client.Client import Client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import base64

def checkJobs(request,token):
    jobs=[]
    projects=[]
    pending_jobs=Deployment_Server.objects.filter(server__token=token,deployed=False).order_by("-id")
    for job in pending_jobs:
        if job.project.name in projects:
            job.deployed=1
            job.save()
            continue
        jobs.append({"id":job.id,"update_type":job.update_type,"update_version":job.update_version,"configFile":base64.encodestring(open(str(job.project.configFile)).read()),
                     "key":job.project.sshKey.key,"workdir":str(job.project.working_dir)
                    ,"scm":job.project.repo_type,"repo":job.project.repo,"project":job.project.name})
        projects=job.project.name
    s=Server.objects.get(token=token)
    s.last_seen=datetime.now()
    s.save()

    return HttpResponse(simplejson.dumps(jobs,indent=True))

def markDone(request,token):
    s=Deployment_Server.objects.get(id=request.GET["id"])
    s.deployed=True
    s.save()
    return HttpResponse("Updated, Thanks.")

def checkServers(request):
    res = {}
    for server in Server.objects.all():
        if server.behindFirewall:
            res[server.name]="Last Seen: %s"% (timezone.now()-server.last_seen).total_seconds()

        else:
            c = Client("git", server.ip, server.port)
            state = c.CheckUp()
            if state:
                res[server.name] = "UP"
            else:
                res[server.name] = "DOWN"
    return HttpResponse(simplejson.dumps(res))

@csrf_protect
def clone(request):
    scm = str(request.GET["scm"])
    ip = str(request.GET["ip"])
    port = int(request.GET["port"])
    project=Project.objects.get(name=request.GET["project_name"])
    c = Client(scm,ip,port,project.sshKey.key)
    res = c.Clone(project.repo, project.working_dir)
    return HttpResponse(res)

@csrf_protect
def deploy(request):
    import Common
    server = Server.objects.get(name=request.session["deploy_server"])
    project = Project.objects.get(name=request.session["deploy_project"])
    D= Deployment_Server()
    c = Client(str(project.repo_type), server.ip, server.port)
    D.project = project
    D.server = server
    D.datetime = timezone.now()
    if "tag" in request.GET:
        D.update_type = "tag"
        D.update_version = request.GET["tag"]
        project.lastTag = request.GET["tag"]
        project.lastUpdate = timezone.now()
    elif "commit" in request.GET:
        D.update_type = "commit"
        D.update_version = request.GET["commit"]
        project.lastCommit = request.GET["commit"]

    if not server.behindFirewall:
        if "tag" in request.GET:
            res = c.SwitchTag(project.working_dir, request.GET["tag"])
        elif "commit" in request.GET:
            if request.GET["commit"] != "HEAD":
                res = c.SwitchCommit(project.working_dir, request.GET["commit"])

        res = c.Deploy(project.working_dir, project.configFile,D.update_type,D.update_version,key=project.sshKey.key)
        if not "ERR:" in res:
            D.deployed=True
            D.has_new_version=False
            D.save()

            project.newVersion=False
            project.save()
            print project.deployment_link
            link=project.deployment_link
            if not "http://" in project.deployment_link:
                print "in if"
                link="http://"+server.DNS+project.deployment_link
            if project.emailUsers!="" or project.emailUsers!=" ":
                try:
                    Common.send(project.emailUsers.replace(",",";"),"New version of %s deployed"%project.name,"Dear User,<br/> This is an automated notification that a new version of %s has been deployed at: %s"%(project.name,link),fromUser=None,cc="",bcc="",)
                except:
                    pass
            return HttpResponse(res+",,"+link)
        else:
                return HttpResponse(res)
    else:
        D.deployed=False
        D.save()
        project.save()
        return HttpResponse("The job is submitted and waiting to the server to pull it")
