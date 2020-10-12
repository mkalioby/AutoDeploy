from django.shortcuts import render
from django_tables2_reports.utils import create_report_http_response
from .forms import *
from deployment.models import Server, SSHKey
from .tables import *
from django_tables2.export.export import TableExport
from django.views.decorators.csrf import csrf_protect
from django_tables2_reports.config import RequestConfigReport
from django_tables2.config import RequestConfig
import sys
sys.path.append("../../../client")
from autodeploy_client import Client
from django.shortcuts import redirect,reverse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from autoDeploy import settings
import simplejson
import ast

@login_required(redirect_field_name="redirect")
def ci_projects(request):
    name = "CI Projects"
    if request.user.is_superuser:
        xlstable = CIProjectReport(CIProject.objects.all())
    else:
        projects = CIUser_Project.objects.filter(user_id=request.user.id).values_list('project', flat=True)
        xlstable = CIProjectReport(CIProject.objects.filter(name__in=list(projects)))
    RequestConfig(request, paginate={"per_page": 15}).configure(xlstable)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, xlstable)
        return exporter.response('table.{}'.format(export_format))
    # table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    # if table_to_report:
    #     return create_report_http_response(table_to_report, request)
    return render(request,"modifyci.html", {"name": name, "table": xlstable})


def add_ci_project(request):
    if request.method == "GET":
        return render(request,"add_ciproject.html", {"form": CIProjectsForm()})
    else:
        form = CIProjectsForm(request.POST, request.FILES)
        if request.POST.get("edit", "False") == "True":
            project = CIProject.objects.get(name=request.POST["name"])
            project.integration_link = request.POST["integration_link"]
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
            return render(request,"add_ciproject.html", {"form": form, "done": True})
        if form.is_valid():
            form.save(request.FILES, form.cleaned_data["name"])
            return render(request,"add_ciproject.html", {"form": form, "done": True})
        else:
            return render(request,"add_ciproject.html", {"form": form, "error": True})


@csrf_protect
@login_required(redirect_field_name="redirect")
def clone(request):
    if request.method == "GET":
        project = CIProject.objects.get(name=request.GET["project"])
        return render(request,"cloneci.html", {"form": CloneForm(initial={"server":project.default_server}), "project_workdir": project.working_dir})
    else:
        project = CIProject.objects.get(name=request.POST["project"])
        form = CloneForm(request.POST)
        if form.is_valid():
            server = Server.objects.get(name=form.cleaned_data["server"])
            token = csrf(request).get("csrf_token")
            data = "{scm: '%s', ip: '%s', port: '%s', project_name: '%s', csrfmiddlewaretoken: '%s' }" % (project.repo_type, server.ip, server.port, project.name, token)
            return render(request,"base.html", {"project": project, "ajax": True, "data": data, "dataType": "html",
                                                    "title": "Cloning " + project.name, "function": "cloneCI"})

@login_required(redirect_field_name="redirect")
@csrf_protect
def integrate(request):
    if request.method == "GET":
        project = CIProject.objects.get(name=request.GET["project"])
        request.session["integrate_project"] = request.GET["project"]
        return render(request,"integrate.html", {"form": CloneForm(initial={"server": project.default_server})})

@login_required(redirect_field_name="redirect")
def integrate2(request):
    server = None
    project = CIProject.objects.get(name=request.session["integrate_project"])
    if request.method == "POST":
        form = CloneForm(request.POST)
        if form.is_valid():
            server = Server.objects.get(name=request.POST["server"])
            request.session["integrate_server"] = request.POST["server"]
        else:
            url = reverse('integrate')+"?project="+request.session["integrate_project"]
            # return HttpResponseRedirect("../integrate?project="+request.session["integrate_project"])
            return HttpResponseRedirect(redirect(url))
    else:
        server = Server.objects.get(name=request.session["integrate_server"])
        if request.GET.get("refresh","False")=="True":
            c=Client(str(project.repo_type), server.ip, server.port, project.sshKey.key)
            c.Pull(project.repo, project.working_dir, project.sshKey.key)
    if project.update_style == "tag":
        return listTags(request, server)
    else:
        filter = request.GET.get("filter", None)
        return listCICommits(request, filter)


@login_required(redirect_field_name="redirect")
def listTags(request, server):
    project = CIProject.objects.get(name=request.session["integrate_project"])
    c = Client(str(project.repo_type), server.ip, server.port, key=project.sshKey.key)
    res = c.ListTags(project.working_dir)
    print(res)
    table = TagTable(res)
    table_to_report = RequestConfig(request, paginate={"per_page": 15}).configure(table)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render(request,"integrate2.html", {"project": project, "count": len(res), "mode": "tags", "tags": table})


@login_required(redirect_field_name="redirect")
def integrate3(request):
    from autoDeploy.api import integrate_core
    if request.method == "GET":
        commit = request.GET.get("commit", None)
        tag = request.GET.get("tag", None)
        project = CIProject.objects.get(name=request.session["integrate_project"])
        server = Server.objects.get(name=request.session["integrate_server"])
        integrate_core(server,project,tag,commit)
        url = reverse('getIntegrationHistory')+"?project="+project.name
        return HttpResponseRedirect(url)

def edit_ci_project(request, project):
    if request.method == "GET":
        project = CIProject.objects.get(name=project)
        form = CIProjectsForm(instance=project)
        return render(request,"add_ciproject.html", {"form": form, "edit": True,'project':project})


def delete_ci_project(request, name):
    if request.method == "GET":
        return render(request,"confirm.html", {"form": "../confirm_delete", "name": name, "type": "CI Project",
                                                   "back_url": "../../"})



@login_required(redirect_field_name="redirect")
def getProjectIntHistory(request):
    project_name = request.GET["project"]
    details = False
    text = "<a href='?project="+project_name+"&details=True'>Show all integration history</a>"
    if "details" in request.GET:
        if request.GET["details"] == "True":
            details = True
            text = "<a href='?project="+project_name+"'>Show latest updates</a>"
    integrations = Integration_server.objects.filter(project__name=project_name).order_by("-datetime")
    res = []
    servers = []
    for integration in integrations:
        if not details and integration.server.name in servers: continue
        servers.append(integration.server.name)
        res.append(integration)
    table = IntegrationHistory(res)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request,"modifyci.html", {"table": table, "name": "Integration for %s" % project_name, "text": text})


def getHistory(request):
    commit = request.GET["commit"]
    integrations = Integration_server.objects.filter(update_version=commit).order_by("-datetime")[:5]
    html = """<tr id="%s">
        <th>Datetime</th>
        <th>Server</th>
        <th>Update type</th>
        <th>Update version</th>
        <th>Result</th>
        <th>Status</th>
    </tr>
    """%(commit)
    for item in integrations:
        result = "<ul>"
        res = simplejson.loads(item.result)
        for k,v in res.items():
            result += "<li>" + v['result'] + "</li>"
        result += "</ul>"
        html += """
        <tr id="%s">
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td><span class="%s-dot" title='%s'></span></td>
        </tr>
        """ % (commit,item.datetime.strftime("%Y-%m-%d %H:%M:%S"), item.server, item.update_type, item.update_version,result,item.status,item.status)
    return HttpResponse(html)

@login_required(redirect_field_name="redirect")
def listCICommits(request, filter=None):
    # if request.method == "GET":
    res = None
    branches = []
    c = None
    error=True
    server = None
    project = None
    project = CIProject.objects.get(name=request.session["integrate_project"])
    if filter == None: filter = project.default_branch if project.default_branch not in ("", None) else None
    print(request.GET.get("refresh", "False"))
    if request.GET.get("refresh", "False") == "True":
        if "commits" in request.session:
            request.session.pop("commits", "")
            request.session.pop("branchs", "")
            return redirect(reverse('ci_commits'))
    if filter or not "commits" in request.session:
        server = Server.objects.get(name=request.session["integrate_server"])

        c = Client("git", server.ip, server.port, key=project.sshKey.key)
        c.Pull(project.repo, project.working_dir, project.sshKey.key)
        res = c.ListCommits(project.working_dir, options={"branch": filter})
        request.session["commits"] = res
    else:
        res = request.session["commits"]
    if not "branchs" in request.session:
        if not c:
            server = Server.objects.get(name=request.session["integrate_server"])
            project = CIProject.objects.get(name=request.session["integrate_project"])
            c = Client("git", server.ip, server.port, key=project.sshKey.key)
        branches = c.ListBranchs(project.working_dir)
    else:
        branches = request.session["branchs"]
        request.session["branchs"] = branches
    context = {"project": project, "mode": "commits", "server": server}
    context["branchs"]=branches
    if not "ERR:" in res:
        table = CommitTable(res)
        context["commits"]=table
    else:
        context["error"] =  res
    # table_to_report = RequestConfig(request, paginate={"per_page": 15}).configure(table)
    # if table_to_report:
    #     return create_report_http_response(table_to_report, request)

    context["current_branch"] = filter
    return render(request,"integrate2.html",context)