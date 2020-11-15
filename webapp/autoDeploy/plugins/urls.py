from django.urls import path as url,re_path
from . import views
urlpatterns = [
    url(r'', views.index, name="plugins_index"),
    url(r'', views.index, name="manage_plugin"),
    url(r'install', views.add_plugin, name="add_plugin"),
    re_path(r'edit/([-@\w]+)/', views.add_plugin, name="edit_plugin"),
    re_path(r'delete/([-@\w]+)/', views.delete_plugin, name="delete_plugin"),

    url(r'checkSlack',views.checkSlack,name="checkSlack"),
    url(r'slack/oauth/',views.slack_oauth,name="slack_oauth"),

]