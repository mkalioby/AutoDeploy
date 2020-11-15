from django.shortcuts import render
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
import requests, json
from . import tables
from . import models
from . import forms


def index(request):
    context = {}
    xlstable = tables.PluginsTable(models.Plugins.objects.all())
    context['table'] = xlstable
    RequestConfig(request, paginate={"per_page": 15}).configure(xlstable)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, xlstable)
        return exporter.response('table.{}'.format(export_format))
    return render(request, "plugins_index.html", context)


def add_plugin(request, plugin_id=None):
    context = {}
    if request.method == 'GET':
        if plugin_id:
            plugin = models.Plugins.objects.get(id=plugin_id)
            form = forms.PluginsForm(initial={"name": plugin.name, "settings": plugin.settings})
            context['plugin_id'] = plugin_id
        else:
            form = forms.PluginsForm()
        context['form'] = form
    else:
        form = forms.PluginsForm(request.POST)
        print("settings => ", form.data['settings'], type(form.data['settings']))
        context['form'] = form
        if request.POST.get("plugin_id", None):
            plugin_id = request.POST['plugin_id']
            context['plugin_id'] = plugin_id
        if form.is_valid():
            plugin = models.Plugins.objects.get(id=plugin_id) if plugin_id else models.Plugins()
            plugin.name = form.data['name']
            plugin.settings = json.loads(form.data['settings'].replace("\'", "\""))
            plugin.save()
            context["done"] = True
        else:
            context['error'] = True
    return render(request, "add_plugin.html", context)


def delete_plugin(request, plugin_id=None):
    plugin = models.Plugins.objects.get(id=plugin_id)
    plugin.delete()
    url = reverse('plugins_index')
    return HttpResponseRedirect(url)


def checkSlack(request):
    context = {}
    plugins = models.Plugins.objects.filter(name__in=['slack', 'Slack'])
    client_id = None
    if plugins.exists():
        plugin = plugins[0]
        client_id = plugin.settings.get("client_id", None)
    context['client_id'] = client_id.replace(" ", "")
    return HttpResponse(json.dumps(context), content_type='application/json')


def slack_oauth(request):
    if "error" in request.GET:
        status = "Oauth authentication failed. You aborted the Authentication process."
        return HttpResponse(status)

    code = request.GET["code"]
    plugin = models.Plugins.objects.get(name="slack")
    url = "https://slack.com/api/oauth.v2.access"
    data = {
        "client_id": plugin.settings.get("client_id", None),
        "client_secret": plugin.settings.get("client_secret", None),
        "code": code,
    }

    r = requests.get(url, params=data)
    query_result = r.json()
    if query_result["ok"]:
        plugin.settings['oauth'] = query_result
        plugin.save()
    else:
        status = "Oauth authentication failed. " + str(query_result['error'])
        return HttpResponse(status)

    status = "Oauth authentication successful!"
    return HttpResponse(status)
