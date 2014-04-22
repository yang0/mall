#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from apps.room import api
from .views import RoomCreate
from .form import RoomForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

urlpatterns = patterns('',
	url(r'^/api$',api.RoomApi.as_view(), name='room_api_create'),
    url(r'^/api/(?P<pk>\d+)$',api.RoomApi.as_view(), name='room_api_detail'),
    url(r'^/api/list$',api.RoomList.as_view(), name='room_api_list'),
    url(r'^$',login_required(RoomCreate.as_view()), name='room_create'),
)
