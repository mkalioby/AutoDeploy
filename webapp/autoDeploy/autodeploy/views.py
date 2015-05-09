from django.shortcuts import render,render_to_response
from django.template import RequestContext
from forms import *
from models import *
from django.views.decorators.csrf import csrf_protect
def projects(request):
    return render_to_response("projects.html",{},context_instance=RequestContext(request))

def add_project(request):
    if request.method=="GET":
        return render_to_response("add_project.html",{"form":addProjectsForm()},context_instance=RequestContext(request))
    else:
        pass
@csrf_protect
def add_server(request):
    if request.method=="GET":
        return render_to_response("add_server.html",{"form":addServerForm},context_instance=RequestContext(request))
    else:
        form=addServerForm(request.POST)
        if form.is_valid:
            form.save()
            return render_to_response("add_server.html",{"form":form,"done":True},context_instance=RequestContext(request))
        else:
            return render_to_response("add_server.html",{"form":form,"error":True},context_instance=RequestContext(request))
