from django.shortcuts import render,render_to_response
from django.template import RequestContext
from forms import *
from models import *
def projects(request):
    return render_to_response("projects.html",{},context_instance=RequestContext(request))

def add_project(request):
    if request.method=="GET":
        return render_to_response("add_project.html",{"form":addProjects},context_instance=RequestContext(request))
    else:
        pass