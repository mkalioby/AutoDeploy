__author__ = 'mohamed'
from django.conf import settings


def global_settings(request):
    # return any necessary values
    # print settings.BASE_URL
    return {
        'STATIC_URL': settings.STATIC_URL,
        'BASE_URL': settings.BASE_URL,
        'TITLE': settings.TITLE
        }