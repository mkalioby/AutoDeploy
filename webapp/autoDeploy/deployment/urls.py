from django.urls import path as url,re_path
from . import views

urlpatterns = [
    url(r'', views.projects, name="cd_index"),
    url(r'add_project/',views.add_project,name='cd_add_project'),
    url(r'clone/',views.clone,name='cd_clone'),
    url(r'getDeploymentHistory/',views.getProjectDepHistory,name='cd_history'),
    url(r'deploy/',views.deploy,name='cd_deploy'),
    url(r'deploy2/',views.deploy2,name='cd_deploy2'),
    url(r'deploy3/',views.deploy3,name='cd_deploy3'),
    url(r'listCommits/',views.listCommits,name='cd_commits'),
    url(r'edit_project/<slug:project>',views.edit_project,name='cd_edit_project'),
    url(r'delete_project/<slug:name>',views.delete_project,name='cd_delete_project'),


]
