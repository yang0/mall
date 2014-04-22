#_*_coding:utf-8_*_
from django.conf import settings
from django import template 



register = template.Library()



@register.filter
def klass(ob):
    return ob.__class__.__name__