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
from django.urls import path as url,include
from django.contrib import admin
from . import views,api
import mfa.TrustedDevice
urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'mfa/', include(('mfa.urls'))),
    url(r'devices/add', mfa.TrustedDevice.add,name="mfa_add_new_trusted_device"),
    url(r'accounts/', include(('accounts.urls'))),
    url(r'', views.index, name="index"),
    url(r'deployment/', include(('deployment.urls'))),
    url(r'integration/', include(('integration.urls'))),

    url(r'add_server', views.add_server,name='add_server'),
    url(r'add_sshkey', views.add_ssh_key,name='add_sshkey'),
    url(r'manage_sshkey', views.manage_ssh_keys, name='manage_sshkey'),
    url(r'edit_sshkey/<slug:sshKey>', views.edit_ssh_key,name='edit_sshkey'),
    url(r'delete_sshkey/<slug:name>', views.delete_ssh_keys,name='delete_sshkey'),
    url(r'confirm_delete', views.confirm_delete,name='confirm_delete'),
    url(r'manage_sshkey', views.manage_ssh_keys, name='manage_sshkey'),
    url(r'checkServers/', views.checkServersStatus,name='checkServers'),
    url(r'manage_servers', views.manage_servers, name='manage_servers'),
    url(r'edit_server/<slug:server>', views.edit_server,name='edit_server'),
    url(r'delete_server/<slug:name>', views.delete_server,name='delete_server'),
    url(r'edit_server/<slug:server>', views.edit_server,name='edit_server'),
    url(r'download_config_file/', views.download_config_file,name='download_config_file'),
    url(r'api/checkServers', api.checkServers, name='api_check_servers'),
    url(r'api/cloneCD', api.cloneCD, name='api_clone_cd'),
    url(r'api/cloneCI', api.cloneCI, name='api_clone_ci'),
    url(r'api/deploy', api.deploy, name='api_deploy'),
    url(r'api/integrate', api.integrate, name='api_integrate'),
    url(r'api/ris', api.receive_integrate_result, name='api_ris'),

]