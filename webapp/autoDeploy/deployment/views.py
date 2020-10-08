from django.shortcuts import render
from django_tables2_reports.utils import create_report_http_response
from .forms import *
from .tables import *
from django_tables2.export.export import TableExport
from django.views.decorators.csrf import csrf_protect
from django_tables2.config import RequestConfig
from autodeploy_client import Client
from django.shortcuts import redirect,reverse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect



@login_required(redirect_field_name="redirect")
def projects(request):
    name = "CD Projects"
    if request.user.is_superuser:
        xlstable = ProjectReport(Project.objects.all())
    else:
        projects = User_Project.objects.filter(user_id=request.user.id).values_list('project', flat=True)
        xlstable = ProjectReport(Project.objects.filter(name__in=list(projects)))
    RequestConfig(request, paginate={"per_page": 15}).configure(xlstable)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, xlstable)
        return exporter.response('table.{}'.format(export_format))
    # table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    # if table_to_report:
    #     return create_report_http_response(table_to_report, request)
    return render(request,"modify.html", {"name": name, "table": xlstable})


@csrf_protect
@login_required(redirect_field_name="redirect")
def add_project(request):
    if request.method == "GET":
        return render(request,"add_project.html", {"form": ProjectsForm()})
    else:
        form = ProjectsForm(request.POST, request.FILES)
        if request.POST.get("edit", "False") == "True":
            project = Project.objects.get(name=request.POST["name"])
            project.deployment_link = request.POST["deployment_link"]
            project.repo = request.POST["repo"]
            project.repo_type = request.POST["repo_type"]
            project.repo_link = request.POST["repo_link"]
            project.sshKey = SSHKey.objects.get(name=request.POST["sshKey"])
            project.working_dir = request.POST["working_dir"]
            project.default_server = Server.objects.get(name=request.POST["default_server"])
            project.update_style = request.POST["update_style"]
            project.emailUsers = request.POST["emailUsers"]
            project.default_branch = request.POST["default_branch"]
            if request.FILES.get("cfile", "") != "":
                project.configFile = saveFile(request.FILES["cfile"], project.name)
            project.save()
            return render(request,"add_project.html", {"form": form, "done": True})
        if form.is_valid():
            form.save(request.FILES, form.cleaned_data["name"])
            return render(request,"add_project.html", {"form": form, "done": True})
        else:
            return render(request,"add_project.html", {"form": form, "error": True})


@csrf_protect
@login_required(redirect_field_name="redirect")
def clone(request):
    if request.method == "GET":
        project = Project.objects.get(name=request.GET["project"])
        return render(request,"clone.html", {"form": CloneForm(initial={"server": project.default_server}),
                                                 "project_workdir": project.working_dir})
    else:
        project = Project.objects.get(name=request.POST["project"])
        form = CloneForm(request.POST)
        if form.is_valid():
            server = Server.objects.get(name=form.cleaned_data["server"])
            token = csrf(request).get("csrf_token")
            data = "{scm: '%s', ip: '%s', port: '%s', project_name: '%s',csrfmiddlewaretoken: '%s' }" % (
            project.repo_type, server.ip, server.port, project.name, token)
            return render(request,"base.html", {"project": project, "ajax": True, "data": data, "dataType": "html",
                                                    "title": "Cloning " + project.name, "function": "cloneCD"})


@login_required(redirect_field_name="redirect")
@csrf_protect
def deploy(request):
    if request.method == "GET":
        project = Project.objects.get(name=request.GET["project"])
        request.session["deploy_project"] = request.GET["project"]
        return render(request,"deploy.html", {"form": CloneForm(initial={"server": project.default_server})})


@login_required(redirect_field_name="redirect")
def deploy2(request):
    server = None
    project = Project.objects.get(name=request.session["deploy_project"])
    if request.method == "POST":
        form = CloneForm(request.POST)
        if form.is_valid():
            server = Server.objects.get(name=request.POST["server"])
            request.session["deploy_server"] = request.POST["server"]
        else:
            return HttpResponseRedirect("../deploy?project=" + request.session["deploy_project"])
    else:
        server = Server.objects.get(name=request.session["deploy_server"])
        if request.GET.get("refresh", "False") == "True":
            c = Client(str(project.repo_type), server.ip, server.port, project.sshKey.key)
            c.Pull(project.repo, project.working_dir, project.sshKey.key)
    if project.update_style == "tag":
        return listTags(request, server)
    else:
        filter = request.GET.get("filter", None)
        return listCommits(request, filter)


@login_required(redirect_field_name="redirect")
def listTags(request, server):
    project = Project.objects.get(name=request.session["deploy_project"])
    c = Client(str(project.repo_type), server.ip, server.port, key=project.sshKey.key)

    res = c.ListTags(project.working_dir)
    print(res)
    table = TagTable(res)
    # table_to_report = RequestConfig(request, paginate={"per_page": 15}).configure(table)
    # if table_to_report:
    #     return create_report_http_response(table_to_report, request)
    return render(request,"deploy2.html", {"project": project, "count": len(res), "mode": "tags", "tags": table})


@login_required(redirect_field_name="redirect")
def deploy3(request):
    if request.method == "GET":
        token = csrf(request).get("csrf_token")
        if "tag" in request.GET:
            data = '{tag:"%s",csrfmiddlewaretoken:"%s"}' % (request.GET["tag"], token)
        elif "commit" in request.GET:
            data = '{"commit":"%s",csrfmiddlewaretoken:"%s"}' % (request.GET["commit"], token)

        project = Project.objects.get(name=request.session["deploy_project"])
        server = Server.objects.get(name=request.session["deploy_server"])
        return render(request,"base.html", {"project": project, "ajax": True, "data": data, "dataType": "html",
                                                "function": "deploy",
                                                "title": "Deploying %s on %s" % (project.name, server.name)})



def edit_project(request, project):
    if request.method == "GET":
        project = Project.objects.get(name=project)
        form = ProjectsForm(instance=project)
        return render(request,"add_project.html", {"form": form, "edit": True,'project':project})


def delete_project(request, name):
    if request.method == "GET":
        return render(request,"confirm.html", {"form": "../confirm_delete", "name": name, "type": "CD Project","back_url": "../../"})


@login_required(redirect_field_name="redirect")
def listCommits(request, filter=None):
    # if request.method == "GET":
    res = None
    branches = []
    c = None
    error=True
    server = None
    project = None
    context = {"project": project, "mode": "commits", "server": server}
    project = Project.objects.get(name=request.session["deploy_project"])
    if filter == None: filter = project.default_branch if project.default_branch not in ("", None) else None
    print(request.GET.get("refresh", "False"))
    if request.GET.get("refresh", "False") == "True":
        if "commits" in request.session:
            request.session.pop("commits", "")
            request.session.pop("branchs", "")
            return redirect(reverse('cd_commits'))
    if filter or not "commits" in request.session:
        server = Server.objects.get(name=request.session["deploy_server"])

        c = Client("git", server.ip, server.port, key=project.sshKey.key)
        c.Pull(project.repo, project.working_dir, project.sshKey.key)
        res = c.ListCommits(project.working_dir, options={"branch": filter})
        request.session["commits"] = res
    else:
        res = request.session["commits"]

    if not "branchs" in request.session:
        if not c:
            server = Server.objects.get(name=request.session["deploy_server"])
            project = Project.objects.get(name=request.session["deploy_project"])
            c = Client("git", server.ip, server.port, key=project.sshKey.key)
        branches = c.ListBranchs(project.working_dir)
    else:
        branches = request.session["branchs"]
        request.session["branchs"] = branches
    context["branchs"] = branches
    if not "ERR:" in res:
        table = CommitTable(res)
        context["commits"] = table
    else:
        context["error"] = res
    # table_to_report = RequestConfig(request, paginate={"per_page": 15}).configure(table)
    # if table_to_report:
    #     return create_report_http_response(table_to_report, request)

    context["current_branch"] = filter
    return render(request,"deploy2.html",context)


@login_required(redirect_field_name="redirect")
def getProjectDepHistory(request):
    project_name = request.GET["project"]
    details = False
    text = text = "<a href='?project=" + project_name + "&details=True'>Show all deployment history</a>"
    if "details" in request.GET:
        if request.GET["details"] == "True":
            details = True
            text = "<a href='?project=" + project_name + "'>Show latest updates</a>"
    deployments = Deployment_Server.objects.filter(project__name=project_name).order_by("-datetime")
    res = []
    servers = []
    for deployment in deployments:
        if not details and deployment.server.name in servers: continue
        servers.append(deployment.server.name)
        c = Client(deployment.project.repo_type, deployment.server.ip, deployment.server.port)
        if deployment.update_type == "commit":
            commits = c.getCommitsDiff(deployment.project.working_dir, deployment.update_version)
            print(commits)
            deployment.has_new_version = len(commits)
            print(deployment.server, deployment.has_new_version)
        res.append(deployment)

    table = DeploymentHistory(res)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request,"modify.html",
                              {"table": table, "name": "Deployments for %s" % project_name, "text": text})
