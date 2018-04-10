from django.shortcuts import render
from django.http import HttpResponse
import simplejson
def hook(request):
    token=request.GET.get("token","")

def push(request):
    return HttpResponse(request.body)


