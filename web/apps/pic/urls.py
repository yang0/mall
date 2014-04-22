#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from apps.pic import api
from .views import PicCreate
from .form import PicForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

urlpatterns = patterns('',
	url(r'^api$',api.PicApi.as_view(), name='pic_api_create'),
    url(r'^api/(?P<pk>\d+)$',api.PicApi.as_view(), name='pic_api_detail'),
    url(r'^api/list$',api.PicList.as_view(), name='pic_api_list'),
    url(r'^$',login_required(PicCreate.as_view()), name='pic_create'),
)
