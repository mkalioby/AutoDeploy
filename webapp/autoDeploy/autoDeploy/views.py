from deployment.forms import *
from deployment.tables import *
from django.views.decorators.csrf import csrf_protect
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
from django.contrib.auth.decorators import login_required
from deployment.views import projects
from deployment.models import *
from integration.models import *
from django.shortcuts import render
from django.http import HttpResponse

@login_required(redirect_field_name="redirect")
def index(request):
    if request.method == "GET":
        return render(request, 'index.html')


@csrf_protect
@login_required(redirect_field_name="redirect")
def add_server(request):
    if request.method == "GET":
        return render(request,"add_server.html", {"form": ServerForm})
    else:
        form = ServerForm(request.POST)
        print(request.POST["edit"])
        if request.POST["edit"] == "True":
            server = Server.objects.get(name=request.POST["name"])
            server.DNS = request.POST["DNS"]
            server.ip = request.POST["ip"]
            server.port = request.POST["port"]
            server.save()
        else:
            if form.is_valid():
                form.save()
            else:
                return render(request,"add_server.html", {"form": form, "error": True})
        return render(request,"add_server.html", {"form": form, "done": True})


@csrf_protect
@login_required(redirect_field_name="redirect")
def add_ssh_key(request):
    if request.method == "GET":
        return render(request,"add_sshkey.html", {"form": SSHKeyForm()})
    else:
        form = SSHKeyForm(request.POST)
        if request.POST["edit"] == "True":
            key = SSHKey.objects.get(name=request.POST["name"])
            key.key = request.POST["key"]
            key.save()
        else:
            if form.is_valid():
                form.save()
            else:
                return render(request,"add_sshkey.html", {"form": form, "error": True})
        return render(request,"add_sshkey.html", {"form": form, "done": True})


@login_required(redirect_field_name="redirect")
def edit_ssh_key(request, sshKey):
    if request.method == "GET":
        key = SSHKey.objects.get(name=sshKey)
        form = SSHKeyForm(instance=key)
        return render(request,"add_sshkey.html", {"form": form, "edit": True})


@login_required(redirect_field_name="redirect")
def edit_server(request, server):
    if request.method == "GET":
        server = Server.objects.get(name=server)
        form = ServerForm(instance=server)
        return render(request,"add_server.html", {"form": form, "edit": True})


@login_required(redirect_field_name="redirect")
def manage_ssh_keys(request):
    name = "SSH Keys"
    xlstable = SSHKeysReport(SSHKey.objects.all())
    RequestConfig(request, paginate={"per_page": 15}).configure(xlstable)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, xlstable)
        return exporter.response('table.{}'.format(export_format))
    # table_to_report = RequestConfigReport(request, paginate={"per_page": 15}).configure(xlstable)
    # if table_to_report:
    #     return create_report_http_response(table_to_report, request)
    return render(request,"modify.html", {"name": name, "table": xlstable})


@login_required(redirect_field_name="redirect")
def manage_servers(request):
    name = "Servers"
    xlstable = ServersReport(Server.objects.all())
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
def delete_ssh_keys(request, name):
    if request.method == "GET":
        return render(request,"confirm.html", {"form": "../confirm_delete", "name": name, "type": "SSH Key",
                                                   "back_url": "./manage_sshkeys"})


@csrf_protect
@login_required(redirect_field_name="redirect")
def delete_server(request, name):
    if request.method == "GET":
        return render(request,"confirm.html", {"form": "../confirm_delete", "name": name, "type": "Server",
                                                   "back_url": "./manage_servers"})


@login_required(redirect_field_name="redirect")
def confirm_delete(request):
    if request.method == "POST":
        n = request.POST["name"]
        if request.POST["type"] == "SSH Key":
            if Project.objects.filter(sshKey__name=n).count() > 0:
                return render(request,"base.html", {"class": "alert alert-danger",
                                                        "text": n + " can NOT be delete as it is linked to another projects."})
            key = SSHKey.objects.get(name=n)
            key.delete()
            return manage_ssh_keys(request)
        elif request.POST["type"] == "Server":
            server = Server.objects.get(name=n)
            server.delete()
            return manage_servers(request)

        elif request.POST["type"] == "CD Project":
            project = Project.objects.get(name=n)
            project.delete()
            return projects(request)

        elif request.POST["type"] == "CI Project":
            project = CIProject.objects.get(name=n)
            project.delete()
            return projects(request)


@login_required(redirect_field_name="redirect")
def checkServersStatus(request):
    # print res
    return render(request,"base.html",
                              {"title": "Servers Health", "function": "checkServers", "dataType": "JSON", "data": "",
                               "ajax": True})


@login_required(redirect_field_name="redirect")
def download_config_file(request):
    file = request.GET["file"]
    import mimetypes
    ctype = mimetypes.guess_type(file)
    response = HttpResponse(content_type=ctype)
    response['Content-Disposition'] = 'attachment; filename=%s' % (file.split("/")[-1])
    response.content = open(file).read()
    return response
