from django.contrib import admin
from django.apps import apps

# Register your models here.
def autoregister(*app_list):
    for model in apps.get_models():
        try:
                admin.site.register(model)
        except Exception:
            pass

autoregister('CI', 'admin')
