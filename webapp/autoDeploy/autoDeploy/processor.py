__author__ = 'mohamed'
from django.conf import settings


def global_settings(request):
    # return any necessary values
    print settings.BASE_URL
    return {
        'BASE_URL': settings.BASE_URL,
        }