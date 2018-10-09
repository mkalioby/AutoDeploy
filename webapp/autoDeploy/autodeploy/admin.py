from django.contrib import admin
from django.apps import apps

# Register your models here.
def autoregister(*app_list):
    for model in apps.get_models():
                admin.site.register(model)

autoregister('autodeploy', 'admin')

