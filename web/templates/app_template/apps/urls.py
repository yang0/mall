#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from apps.{{modelClazz|lower}} import api
from .views import {{ modelClazz }}Create
from .form import {{ modelClazz }}Form
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

urlpatterns = patterns('',
	url(r'^/api$',api.{{ modelClazz }}Api.as_view(), name='{{ modelClazz |lower }}_api_create'),
    url(r'^/api/(?P<pk>\d+)$',api.{{ modelClazz }}Api.as_view(), name='{{ modelClazz |lower }}_api_detail'),
    url(r'^/api/list$',api.{{ modelClazz }}List.as_view(), name='{{ modelClazz |lower }}_api_list'),
    url(r'^$',login_required({{ modelClazz }}Create.as_view()), name='{{ modelClazz |lower }}_create'),
)
