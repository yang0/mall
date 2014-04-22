#_*_coding:utf-8_*_

from django.conf import settings

def my_settings(request):
    return {'DOWNLOAD':settings.DOWNLOAD}
