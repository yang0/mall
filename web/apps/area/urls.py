#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from .api import CityDetail, CityChildren, CityDescendants, SchoolList, SchoolCreate, CityAncestors
from django.contrib.auth.decorators import login_required



urlpatterns = patterns('',
    #url(r'^$',TemplateView.as_view(template_name="enquiry/index.html"), name='enquiry_index'),
    url(r'^cityList/(?P<parentId>\d+)$',cache_page(60*60*1000)(CityChildren.as_view()), name='city_children'),
    url(r'^cityDescendants/(?P<parentId>\d+)$',cache_page(60*60*1000)(CityDescendants.as_view()), name='city_descendants'),
    url(r'^cityAncestors/(?P<cityId>\d+)$',cache_page(60*60*1000)(CityAncestors.as_view()), name='city_ancestors'),
    url(r'^city/(?P<pk>\d+)$',cache_page(60*60*1000)(CityDetail.as_view()), name='city_detail'),
)
