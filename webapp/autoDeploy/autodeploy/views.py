from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django_tables2_reports.utils import create_report_http_response
from forms import *
from models import Project, Server, SSHKey
from tables import *
from django.views.decorators.csrf import csrf_protect
from django_tables2_reports.config import RequestConfigReport
from django_tables2.config import RequestConfig
from autodeploy_client import Client
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required(redirect_field_name="redirect")
def projects(request):
    name = "Projects"
    xlstable = ProjectReport(Project.objects.all())
    table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render_to_response("modify.html", {"name": name, "table": xlstable},
                              context_instance=RequestContext(request))


@csrf_protect
@login_required(redirect_field_name="redirect")
def add_project(request):
    if request.method == "GET":
        return render_to_response("add_project.html", {"form": ProjectsForm()},
                                  context_instance=RequestContext(request))
    else:
        form = ProjectsForm(request.POST, request.FILES)
        if request.POST.get("edit","False") == "True":
            project=Project.objects.get(name=request.POST["name"])
            project.deployment_link=request.POST["deployment_link"]
            project.repo=request.POST["repo"]
            project.repo_type=request.POST["repo_type"]
            project.repo_link=request.POST["repo_link"]
            project.sshKey=SSHKey.objects.get(name=request.POST["sshKey"])
            project.working_dir=request.POST["working_dir"]
            project.default_server=Server.objects.get(name=request.POST["default_server"])
            project.update_style=request.POST["update_style"]
            project.emailUsers=request.POST["emailUsers"]
            if request.FILES.get("cfile","")!="":
                project.configFile=saveFile(request.FILES["cfile"],project.name)
            project.save()
            return render_to_response("add_project.html", {"form": form, "done": True},
                                      context_instance=RequestContext(request))
        if form.is_valid():
            form.save(request.FILES, form.cleaned_data["name"])
            return render_to_response("add_project.html", {"form": form, "done": True},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response("add_project.html", {"form": form, "error": True},
                                      context_instance=RequestContext(request))


@csrf_protect
@login_required(redirect_field_name="redirect")
def add_server(request):
    if request.method == "GET":
        return render_to_response("add_server.html", {"form": ServerForm}, context_instance=RequestContext(request))
    else:
        form = ServerForm(request.POST)
        print request.POST["edit"]
        if request.POST["edit"] == "True":
                server=Server.objects.get(name=request.POST["name"])
                server.DNS=request.POST["DNS"]
                server.ip=request.POST["ip"]
                server.port=request.POST["port"]
                server.behindFirewall=request.POST["behindFirewall"]
                server.token=request.POST["token"]
                server.save()
                if request.POST["behindFirewall"]:
                    from  autodeploy_client.Client import Client
                    if Client.addServer(server.name,server.token) !="Saved":
                        return render_to_response("add_server.html", {"form": form, "error": True},
                                      context_instance=RequestContext(request))


        else:
            if form.is_valid():
                if request.POST["behindFirewall"]:
                    from  autodeploy_client.Client import Client
                    c = Client("git", server.ip, server.port)
                    if c.addServer(request.POST["name"],request.POST["token"])!='Saved':
                        return render_to_response("add_server.html", {"form": form, "error": True},
                                      context_instance=RequestContext(request))

                form.save()

            else:
                return render_to_response("add_server.html", {"form": form, "error": True},
                                      context_instance=RequestContext(request))
        return render_to_response("add_server.html", {"form": form, "done": True},
                                      context_instance=RequestContext(request))



@csrf_protect
@login_required(redirect_field_name="redirect")
def add_ssh_key(request):
    if request.method == "GET":
        return render_to_response("add_sshkey.html", {"form": SSHKeyForm()}, context_instance=RequestContext(request))
    else:
        form = SSHKeyForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response("add_sshkey.html", {"form": form, "done": True},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response("add_sshkey.html", {"form": form, "error": True},
                                      context_instance=RequestContext(request))


@csrf_protect
@login_required(redirect_field_name="redirect")
def clone(request):
    if request.method == "GET":
        project = Project.objects.get(name=request.GET["project"])
        return render_to_response("clone.html", {"form": CloneForm, "project_workdir": project.working_dir},
                                  context_instance=RequestContext(request))
    else:
        project = Project.objects.get(name=request.POST["project"])
        form = CloneForm(request.POST)
        if form.is_valid():
            server = Server.objects.get(name=form.cleaned_data["server"])
            token=csrf(request).get("csrf_token")
            data="{scm: '%s', ip: '%s', port: '%s', project_name: '%s',csrfmiddlewaretoken: '%s' }" % (project.repo_type,server.ip,server.port,project.name,token)
            return render_to_response("base.html", {"ajax":True, "data": data, "dataType":"html",
                                                    "title":"Cloning "+ project.name, "function":"clone"}, context_instance=RequestContext(request))

@login_required(redirect_field_name="redirect")
@csrf_protect
def deploy(request):
    if request.method == "GET":
        request.session["deploy_project"] = request.GET["project"]
        return render_to_response("deploy.html", {"form": CloneForm}, context_instance=RequestContext(request))

@login_required(redirect_field_name="redirect")
def deploy2(request):
    server = None
    project=Project.objects.get(name=request.session["deploy_project"])
    if request.method == "POST":
        form=CloneForm(request.POST)
        if form.is_valid():
            server = Server.objects.get(name=request.POST["server"])
            request.session["deploy_server"] = request.POST["server"]
        else:
            return HttpResponseRedirect("../deploy?project="+request.session["deploy_project"])
    else:
        server = Server.objects.get(name=request.session["deploy_server"])
        if request.GET.get("refresh","False")=="True":
            c=Client(str(project.repo_type),server.ip,server.port,project.sshKey.key)
            c.Pull(project.repo,project.working_dir,project.sshKey.key)
    if project.update_style=="tag":
        return listTags(request, server)
    else:
        return listCommits(request)

@login_required(redirect_field_name="redirect")
def listTags(request, server):
    project = Project.objects.get(name=request.session["deploy_project"])
    c = Client(str(project.repo_type), server.ip, server.port,key=project.sshKey.key)

    res = c.ListTags(project.working_dir)
    print res
    table=TagTable(res)
    table_to_report = RequestConfig(request, paginate={"per_page": 15}).configure(table)
    if table_to_report:
            return create_report_http_response(table_to_report, request)
    return render_to_response("deploy2.html", {"count":len(res),"mode":"tags","tags":table}, context_instance=RequestContext(request))

@login_required(redirect_field_name="redirect")
def deploy3(request):
    if request.method == "GET":
        token=csrf(request).get("csrf_token")
        if "tag" in request.GET:
            data='{tag:"%s",csrfmiddlewaretoken:"%s"}'%(request.GET["tag"],token)
        elif "commit" in request.GET:
            data='{"commit":"%s",csrfmiddlewaretoken:"%s"}'%(request.GET["commit"],token)

        project=Project.objects.get(name=request.session["deploy_project"])
        server=Server.objects.get(name=request.session["deploy_server"])
        return render_to_response("base.html", {"ajax": True,"data":data,"dataType":"html","function":"deploy","title":"Deploying %s on %s"%(project.name,server.name)}, context_instance=RequestContext(request))

@login_required(redirect_field_name="redirect")
def edit_ssh_key(request, sshKey):
    if request.method == "GET":
        key = SSHKey.objects.get(name=sshKey)
        form = SSHKeyForm(instance=key)
        return render_to_response("add_sshkey.html", {"form": form}, context_instance=RequestContext(request))

@login_required(redirect_field_name="redirect")
def edit_server(request, server):
    if request.method == "GET":
        server= Server.objects.get(name=server)
        form = ServerForm(instance=server)
        return render_to_response("add_server.html", {"form": form,"edit":True}, context_instance=RequestContext(request))


def edit_project(request, project):
    if request.method == "GET":
        project= Project.objects.get(name=project)
        form = ProjectsForm(instance=project)
        return render_to_response("add_project.html", {"form": form,"edit":True}, context_instance=RequestContext(request))


@login_required(redirect_field_name="redirect")
def manage_ssh_keys(request):
    name = "SSH Keys"
    xlstable = SSHKeysReport(SSHKey.objects.all())
    table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render_to_response("modify.html", {"name": name, "table": xlstable},
                              context_instance=RequestContext(request))

@login_required(redirect_field_name="redirect")
def manage_servers(request):
    name = "Servers"
    xlstable = ServersReport(Server.objects.all())
    table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render_to_response("modify.html", {"name": name, "table": xlstable},
                              context_instance=RequestContext(request))

@csrf_protect
@login_required(redirect_field_name="redirect")
def delete_ssh_keys(request, name):
    if request.method == "GET":
        return render_to_response("confirm.html", {"form": "../confirm_delete", "name": name, "type": "SSH Key",
                                                   "back_url": "./manage_sshkeys"},
                                  context_instance=RequestContext(request))

@csrf_protect
@login_required(redirect_field_name="redirect")
def delete_server(request, name):
    if request.method == "GET":
        return render_to_response("confirm.html", {"form": "../confirm_delete", "name": name, "type": "Server",
                                                   "back_url": "./manage_servers"},
                                  context_instance=RequestContext(request))


def delete_project(request, name):
    if request.method == "GET":
        return render_to_response("confirm.html", {"form": "../confirm_delete", "name": name, "type": "Project",
                                                   "back_url": "../../"},
                                  context_instance=RequestContext(request))


@login_required(redirect_field_name="redirect")
def confirm_delete(request):
    if request.method == "POST":
        n = request.POST["name"]
        if request.POST["type"] == "SSH Key":
            if Project.objects.filter(sshKey__name=n).count() > 0:
                return render_to_response("base.html", {"class": "alert alert-danger",
                                                        "text": n + " can NOT be delete as it is linked to another projects."},
                                          context_instance=RequestContext(request))
            key = SSHKey.objects.get(name=n)
            key.delete()
            return manage_ssh_keys(request)
        elif request.POST["type"]=="Server":
            server=Server.objects.get(name=n)
            server.delete()
            return manage_servers(request)

        elif request.POST["type"]=="Project":
            project=Project.objects.get(name=n)
            project.delete()
            return projects(request)




@login_required(redirect_field_name="redirect")
def checkServersStatus(request):

    # print res
    return render_to_response("base.html", {"title":"Servers Health","function":"checkServers","dataType":"JSON","data":"","ajax": True}, context_instance=RequestContext(request))

@login_required(redirect_field_name="redirect")
def listCommits(request):
    #if request.method == "GET":
    res = None
    print request.GET.get("refresh","False")
    if request.GET.get("refresh","False")=="True":
        if "commits" in request.session:
            del request.session["commits"]
            return redirect("./listCommits")
    if not "commits" in request.session:
        server = Server.objects.get(name=request.session["deploy_server"])
        project = Project.objects.get(name=request.session["deploy_project"])
        c = Client("git", server.ip, server.port,key=project.sshKey.key)
        c.Pull(project.repo,project.working_dir,project.sshKey.key)
        res = c.ListCommits(project.working_dir)
        print res
        request.session["commits"] = res
    else:
        res = request.session["commits"]
    table = CommitTable(res)
    table_to_report = RequestConfig(request, paginate={"per_page": 15}).configure(table)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render_to_response("deploy2.html", {"mode":"commits","commits": table}, context_instance=RequestContext(request))


@login_required(redirect_field_name="redirect")
def getProjectDepHistory(request):
    project_name=request.GET["project"]
    details=False
    text=text="<a href='?project="+project_name+"&details=True'>Show all deployment history</a>"
    if "details" in request.GET:
        if request.GET["details"]=="True":
            details=True
            text="<a href='?project="+project_name+"'>Show latest updates</a>"
    deployments=Deployment_Server.objects.filter(project__name=project_name).order_by("-datetime")
    res=[]
    servers=[]
    for deployment in deployments:
        if not details and deployment.server.name in servers: continue
        servers.append(deployment.server.name)
        c = Client(deployment.project.repo_type, deployment.server.ip, deployment.server.port)
        if deployment.update_type == "commit":
            commits=c.getCommitsDiff(deployment.project.working_dir,deployment.update_version)
            print commits
            deployment.has_new_version = len(commits)
            print deployment.server,deployment.has_new_version
        res.append(deployment)


    table=DeploymentHistory(res)
    RequestConfigReport(request, paginate={"per_page": 15}).configure(table)
    return render_to_response("modify.html",{"table":table,"name": "Deployments for %s"%project_name,"text":text},context_instance=RequestContext(request))