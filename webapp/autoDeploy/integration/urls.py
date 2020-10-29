from django.urls import path as url,re_path
from . import views

urlpatterns = [
    url(r'', views.ci_projects, name="ci_index"),
    url(r'add_ciproject', views.add_ci_project, name="ci_add_project"),
    url(r'cloneci/', views.clone,name='cloneci'),
    url(r'getIntegrationHistory/', views.getProjectIntHistory,name='getIntegrationHistory'),
    url(r'getHistory/', views.getHistory,name='getHistory'),
    re_path(r'getShow/(\w+)', views.getHistory,name='getShow'),
    url(r'integrate/', views.integrate,name='integrate'),
    url(r'integrate2/', views.integrate2,name='integrate2'),
    url(r'integrate3/', views.integrate3,name='integrate3'),
    re_path(r'^edit_ciproject/([-@\w]+)/', views.edit_ci_project, name="edit_ciproject"),
    re_path(r'^delete_ciproject/([-@\w]+)/', views.delete_ci_project, name="delete_ciproject"),
    url(r'listCommits/',views.listCICommits,name='ci_commits'),
    re_path(r'status/(\w+)',views.status,name='ci_status'),
    re_path(r'coverage/(\w+)',views.coverage,name='ci_coverage'),
    re_path(r'webhooks/',views.webhooks,name='webhooks'),
]