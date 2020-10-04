__author__ = 'mohamed'

from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'login',views.check,name='login'),
    url(r'logout',views.signOut,name='logout'),

]
