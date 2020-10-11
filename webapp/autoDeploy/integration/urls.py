from django.urls import path as url,re_path
from . import views

urlpatterns = [
    url(r'', views.ci_projects, name="ci_index"),
    url(r'add_ciproject', views.add_ci_project, name="ci_add_project"),
    url(r'cloneci/', views.clone,name='cloneci'),
    url(r'getIntegrationHistory/', views.getProjectIntHistory,name='getIntegrationHistory'),
    url(r'getHistory/', views.getHistory,name='getHistory'),
    url(r'integrate/', views.integrate,name='integrate'),
    url(r'integrate2/', views.integrate2,name='integrate2'),
    url(r'integrate3/', views.integrate3,name='integrate3'),
    re_path('edit_ciproject/(\w+)/', views.edit_ci_project, name="edit_ciproject"),
    re_path('delete_ciproject/(\w+)/', views.delete_ci_project, name="delete_ciproject"),
    url(r'listCommits/',views.listCICommits,name='ci_commits'),
]