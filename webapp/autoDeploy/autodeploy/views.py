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
    name="Projects"
    xlstable=ProjectReport(Project.objects.all())
    table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render_to_response("modify.html",{"name":name,"table":xlstable},context_instance=RequestContext(request))
@csrf_protect
def add_project(request):
    if request.method=="GET":
        return render_to_response("add_project.html",{"form":ProjectsForm()},context_instance=RequestContext(request))
    else:
        form=ProjectsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(request.FILES,form.cleaned_data["name"])
            return render_to_response("add_project.html",{"form":form,"done":True},context_instance=RequestContext(request))
        else:
            return render_to_response("add_project.html",{"form":form,"error":True},context_instance=RequestContext(request))
@csrf_protect
def add_server(request):
    if request.method=="GET":
        return render_to_response("add_server.html",{"form":ServerForm},context_instance=RequestContext(request))
    else:
        form=ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response("add_server.html",{"form":form,"done":True},context_instance=RequestContext(request))
        else:
            return render_to_response("add_server.html",{"form":form,"error":True},context_instance=RequestContext(request))

@csrf_protect
def add_ssh_key(request):
    if request.method=="GET":
        return render_to_response("add_sshkey.html",{"form":SSHKeyForm()},context_instance=RequestContext(request))
    else:
        form=SSHKeyForm(request.POST)
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

def edit_ssh_key(request, sshKey):
    if request.method=="GET":
        key=SSHKey.objects.get(name=sshKey)
        form=SSHKeyForm(instance=key)
        return render_to_response("add_sshkey.html",{"form":form},context_instance=RequestContext(request))

def manage_ssh_keys(request):
    name="SSH Keys"
    xlstable=SSHKeysReport(SSHKey.objects.all())
    table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render_to_response("modify.html",{"name":name,"table":xlstable},context_instance=RequestContext(request))

@csrf_protect
def delete_ssh_keys(request,name):
    if request.method=="GET":
        return render_to_response("confirm.html",{"form":"../confirm_delete","name":name,"type":"SSH Key","back_url":"./manage_sshkys"},context_instance=RequestContext(request))

def confirm_delete(request):
    if request.method=="POST":
        n=request.POST["name"]
        if request.POST["type"]=="SSH Key":
            if Project.objects.filter(sshKey__name=n).count()>0:
                return render_to_response("base.html",{"class":"alert alert-danger","text":n+" can NOT be delete as it is linked to another projects."},context_instance=RequestContext(request))
            key=SSHKey.objects.get(name=n)
            key.delete()
            return manage_ssh_keys(request)
