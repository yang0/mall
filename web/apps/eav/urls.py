#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from apps.eav import api
from .views import EavPropCreate
from .form import EavPropForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

urlpatterns = patterns('',
	url(r'^/api$',api.EavPropApi.as_view(), name='eavprop_api_create'),
    url(r'^/api/(?P<pk>\d+)$',api.EavPropApi.as_view(), name='eavprop_api_detail'),
    url(r'^/api/list$',api.EavPropList.as_view(), name='eavprop_api_list'),
    url(r'^/api/enumgroup/(?P<pk>\d+)$',api.EavEnumGroupApi.as_view(), name='eavgroup_api_detail'),
    url(r'^$',login_required(EavPropCreate.as_view()), name='eavprop_create'),
)
