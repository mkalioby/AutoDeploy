from django.shortcuts import render
from django_tables2_reports.utils import create_report_http_response
from .forms import *
from deployment.models import Server, SSHKey
from .tables import *
from django_tables2.export.export import TableExport
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django_tables2.config import RequestConfig
import sys
sys.path.append("../../../client")
from autodeploy_client import Client
from django.shortcuts import redirect,reverse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,Http404
from autoDeploy import settings
import os.path
import json

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
    context = {}
    if request.method == "GET":
        context['form'] = CIProjectsForm()
    else:
        form = CIProjectsForm(request.POST, request.FILES)
        context["form"] = form
        if request.POST.get("edit", "False") == "True":
            project = CIProject.objects.get(name=request.POST["name"])
            # project.integration_link = request.POST["integration_link"]
            project.repo = request.POST["repo"]
            project.repo_type = request.POST["repo_type"]
            project.repo_link = request.POST["repo_link"]
            project.sshKey = SSHKey.objects.get(name=request.POST["sshKey"])
            project.working_dir = request.POST["working_dir"]
            project.default_server = Server.objects.get(name=request.POST["default_server"])
            project.update_style = request.POST["update_style"]
            project.emailUsers = request.POST["emailUsers"]
            project.default_branch = request.POST["default_branch"]
            project.slackchannel = request.POST["slackchannel"]
            if request.FILES.get("cfile2", "") != "":
                project.configFile = saveFile(request.FILES["cfile2"], project.name)
            elif request.POST['cfile'] == 'branch':
                project.configFile = None
            project.save()
            context["done"] = True
        else:
            if form.is_valid():
                form.save(request.FILES, form.cleaned_data["name"])
                context["done"] = True
            else:
                context['error'] = True
    return render(request,"add_ciproject.html", context)


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
        url = reverse('getShow',args=[project.name])
        return HttpResponseRedirect(url)

def edit_ci_project(request, project):
    if request.method == "GET":
        project = CIProject.objects.get(name=project)
        file_name = project.configFile.name.split('/')[-1]
        config_file = project.name+'/'+ file_name if project.configFile not in ['',None] and os.path.exists(project.configFile.path) else None
        form = CIProjectsForm(instance=project)
        return render(request,"add_ciproject.html", {"form": form, "edit": True,'project':project,"config_file":config_file,"file_name":file_name})


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


def getHistory(request,project_name=None):
    context = {}
    requested_project = project_name if project_name else request.GET["project"]
    project = CIProject.objects.filter(name=requested_project)
    if project.exists():
        project = project[0]
        context['branch'] = project.default_branch
        context['integrations'] = Integration_server.objects.filter(project__name=project).order_by("-datetime")[:5]
        context['project_name'] = project
        dir_list = []
        for item in context['integrations']:
            dir_name = str(project) + '/' + str(item.id)
            folderDir = settings.ARTIFACTOR_DIR + '/' + dir_name
            if os.path.isdir(folderDir):
                dir_list.append({'processDir':  os.listdir(folderDir), 'processId': item.id, 'folders': dir_name})
        context['dir_list'] = dir_list

    else:
        context['error'] = "Project ( %s ) cannot be found"%(requested_project)
    return render(request,"integration_history.html",context)

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

@csrf_exempt
def status(request,project_name):
    project = CIProject.objects.filter(name=project_name)
    if project.exists():
        project = project[0]
        IS = Integration_server.objects.filter(project__name=project)
        if IS.exists():
            IS_status = IS.order_by("-datetime")[0]
            status = IS_status.status
            url = 'https://img.shields.io/badge/build-{}-{}'
            if status.code == 0: url = url.format(status.description,'lightgrey')
            if status.code == 1: url = url.format(status.description,'orange')
            if status.code == 2: url = url.format(status.description,'brightgreen')
            if status.code == 3: url = url.format(status.description,'red')
            return HttpResponseRedirect(url)
        else:
            raise Http404("Project has no running tests")
    else:
        raise Http404("Project does not exist")

@csrf_exempt
def coverage(request,project_name):
    project = CIProject.objects.filter(name=project_name)
    if project.exists():
        project = project[0]
        url = coverage_core(project_name=project.name)
        if url != '':
            return HttpResponseRedirect(url)
        else:
            raise Http404("Project has no running tests")
    else:
        raise Http404("Project does not exist")

def coverage_core(project_name=None,commit=None):
    url = ""
    if project_name:
        IS = Integration_server.objects.filter(project__name=project_name)
    else:
        IS = Integration_server.objects.filter(id=commit)
    if IS.exists():
        IS_Coverage = IS.order_by("-datetime")[0].coverage
        if IS_Coverage and IS_Coverage != '-i.':
            coverage = int(IS_Coverage.replace("%",""))
            url = 'https://img.shields.io/badge/coverage-{}%25-{}'
            if 85 < coverage <= 100: url = url.format(coverage, 'brightgreen')
            elif 70 < coverage <= 85: url = url.format(coverage, 'green')
            elif 60 < coverage <= 70: url = url.format(coverage, 'yellowgreen')
            elif 50 < coverage <= 60: url = url.format(coverage, 'yellow')
            elif 40 < coverage <= 50: url = url.format(coverage, 'orange')
            elif 25 < coverage <= 40: url = url.format(coverage, 'red')
            else: url = url.format(coverage, 'lightgrey')
        else:
            url = 'https://img.shields.io/badge/coverage-inactive-inactive'
    return url

@csrf_exempt
def webhooks(request):
    import json
    msg = "This is webhooks function."
    print(msg," \n ",request.body)
    return HttpResponse(json.dumps(msg))


def getProcessResults(request, process_id):
    process = Integration_server.objects.get(id=process_id)
    html = "<ul>"
    html2 = "<table id='table-body'><tbody>"
    if process.result:
        for k,v in process.result.items():
            html += "<li><strong>Server :</strong> " + str(process.server) + "</li>"
            html += """
                <li><strong>Command :</strong> %s </li>
                <li><strong>Exit Code :</strong> %s </li>
                <li><strong>Result :</strong> <div class="result-div"></div>
                """ % (k, v['exit_code'])
            if process.status_id == 2:
                html += "<div class='alert alert-success'><pre>%s</pre></div>" % (v['result'])
            elif process.status_id == 3:
                html += "<div class='alert alert-danger'><pre>%s</pre></div>" % (v['result'])
            else:
                html += "<pre>%s</pre>" %(v['result'])
            html += "</li>"
        html2 += "<td><span class='glyphicon glyphicon-plus'></span> " + process.datetime.strftime("%Y-%m-%d %H:%I") + "</td>"
        html2 += "<td>" + str(process.branch) + "</td>"
        html2 += "<td>" + str(process.update_type) + "</td>"
        html2 += "<td id='update_version'>" + str(process.update_version) + "</td>"
        if process.author_name:
            html2 += "<td>" + str(process.author_name) + "</td>"
        html2 += "<td><div style='padding-top: 7%'><span class= '" + str(process.status) + "-dot 'title='" + str(process.status) + "'></span><img src='" + str(process.get_coverage()) + "' id='coverage'/></div></td>"
    html2 += "<tbody></table>"
    html += "</ul>"
    return HttpResponse(json.dumps({'html1':html,"html2":html2}), content_type="application/json")
