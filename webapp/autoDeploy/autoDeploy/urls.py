"""autoDeploy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import accounts.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^$','autodeploy.views.projects'),
    url(r'add_project','autodeploy.views.add_project'),
    url(r'add_server','autodeploy.views.add_server'),
    url(r'add_sshkey','autodeploy.views.add_ssh_key'),
    url(r'manage_sshkey','autodeploy.views.manage_ssh_keys', name='mange_sshkeys'),
    url(r'edit_sshkey/(\w+)','autodeploy.views.edit_ssh_key'),
    url(r'delete_sshkey/(\w+)','autodeploy.views.delete_ssh_keys'),
    url(r'confirm_delete','autodeploy.views.confirm_delete'),
    url(r'manage_sshkey','autodeploy.views.manage_ssh_keys', name='mange_sshkeys'),
    url(r'clone/','autodeploy.views.clone'),
    url(r'getDeploymentHistory/','autodeploy.views.getProjectDepHistory'),
    url(r'deploy/','autodeploy.views.deploy'),
    url(r'deploy2/','autodeploy.views.deploy2'),
    url(r'deploy3/','autodeploy.views.deploy3'),
    url(r'checkServers/','autodeploy.views.checkServersStatus'),
    url(r'check/(\w+)','autodeploy.api.checkJobs'),
    url(r'notify/(\w+)','autodeploy.api.markDone'),
    url(r'listCommits/','autodeploy.views.listCommits'),
    url(r'manage_servers','autodeploy.views.manage_servers', name='mange_sshkeys'),
    url(r'edit_server/(\w+)','autodeploy.views.edit_server'),
    url(r'delete_server/(\w+)','autodeploy.views.delete_server'),
    url(r'edit_server/(\w+)','autodeploy.views.edit_server'),
    url(r'edit_project/(\w+)','autodeploy.views.edit_project'),
    url(r'delete_project/(\w+)','autodeploy.views.delete_project'),


    url(r'api/checkServers','autodeploy.api.checkServers'),
    url(r'api/clone','autodeploy.api.clone'),
    url(r'api/deploy','autodeploy.api.deploy'),

]
