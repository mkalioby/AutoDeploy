from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'hook',views.hook),
    url(r'hook/push',views.push),
    ]
