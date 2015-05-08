from django.shortcuts import render,render_to_response
from django.template import RequestContext
def projects(request):
    return render_to_response("projects.html",{},context_instance=RequestContext(request))