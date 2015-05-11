from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django_tables2_reports.utils import create_report_http_response
from forms import *
from models import *
from tables import *
from django.views.decorators.csrf import csrf_protect
from django_tables2_reports.config import RequestConfigReport
from client.Client import Client
from django.shortcuts import redirect

def projects(request):
    xlstable=ProjectReport(Project.objects.all())
    table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    print xlstable
    return render_to_response("projects.html",{"table":xlstable},context_instance=RequestContext(request))
@csrf_protect
def add_project(request):
    if request.method=="GET":
        return render_to_response("add_project.html",{"form":addProjectsForm()},context_instance=RequestContext(request))
    else:
        form=addProjectsForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response("add_project.html",{form:form,"done":True},context_instance=RequestContext(request))
        else:
            return render_to_response("add_project.html",{form:form,"error":True},context_instance=RequestContext(request))
@csrf_protect
def add_server(request):
    if request.method=="GET":
        return render_to_response("add_server.html",{"form":addServerForm},context_instance=RequestContext(request))
    else:
        form=addServerForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response("add_server.html",{"form":form,"done":True},context_instance=RequestContext(request))
        else:
            return render_to_response("add_server.html",{"form":form,"error":True},context_instance=RequestContext(request))

@csrf_protect
def add_ssh_key(request):
    if request.method=="GET":
        return render_to_response("add_sshkey.html",{"form":addSSHKeyForm()},context_instance=RequestContext(request))
    else:
        form=addSSHKeyForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response("add_sshkey.html",{"form":form,"done":True},context_instance=RequestContext(request))
        else:
            return render_to_response("add_sshkey.html",{"form":form,"error":True},context_instance=RequestContext(request))

@csrf_protect
def clone(request):
    if request.method=="GET":
        project=Project.objects.get(name=request.GET["project"])
        return render_to_response("clone.html",{"form":CloneForm,"project_workdir":project.working_dir},context_instance=RequestContext(request))
    else:
        project=Project.objects.get(name=request.POST["project"])
        form=CloneForm(request.POST)
        if form.is_valid:
            c=Client("git")
            res=c.Clone(project.repo,project.working_dir,project.sshKey.key)
            print res
            return render_to_response("clone.html",{"form":form,"result":res},context_instance=RequestContext(request))

@csrf_protect
def deploy(request):
    if request.method=="GET":
        request.session["deploy_project"]=request.GET["project"]
        return render_to_response("deploy.html",{"form":CloneForm},context_instance=RequestContext(request))
    else:
        request.session["deploy_server"]=request.POST["server"]
        return redirect("../deploy2/")
def deploy2(request):
    if request.method=="GET":
        c=Client("git")
        project=Project.objects.get(name=request.session["deploy_project"])
        res=c.ListTags(project.working_dir)
        return render_to_response("deploy2.html",{"tags":res.split("\n")},context_instance=RequestContext(request))
def deploy3(request):
    if request.method=="GET":
        c=Client("git")
        project=Project.objects.get(name=request.session["deploy_project"])
        res=c.SwitchTag(project.working_dir,request.GET["tag"])
        res=c.Deploy(project.working_dir,project.configFile)
        return render_to_response("deploy2.html",{"result":res},context_instance=RequestContext(request))

