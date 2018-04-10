from django.conf.urls import include, url
from django.contrib import admin
import accounts,webHooks

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^hooks/', include(webHooks.urls)),
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
