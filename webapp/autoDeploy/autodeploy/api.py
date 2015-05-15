__author__ = 'mohamed'
from models import *
import simplejson
from  client.Client import Client
from django.http import HttpResponse

def checkServers(request):
    res = {}
    for server in Server.objects.all():
        c = Client("git", server.ip, server.port)
        state = c.CheckUp()
        #d = {"name": server.name}
        if state:
            res[server.name] = "UP"
        else:
            res[server.name] = "DOWN"
    return HttpResponse(simplejson.dumps(res))