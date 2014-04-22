#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from apps.product import api
from .views import ProductItemCreate, ProductItemCreate_deprecate
from .form import ProductItemForm, ProductItemForm_wiard1, ProductItemForm_wiard2
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

urlpatterns = patterns('',
	url(r'^/api$',api.ProductItemApi.as_view(), name='productitem_api_create'),
    url(r'^/api/(?P<pk>\d+)$',api.ProductItemApi.as_view(), name='productitem_api_detail'),
    url(r'^/api/list$',api.ProductItemList.as_view(), name='productitem_api_list'),
    url(r'^/api/categoryProps/(?P<pk>\d+)$',api.CategoryProps.as_view(), name='category_props'),

    #该方法基于formwizard方式创建商品，弃用，仅供以后编码参考
    url(r'^/testCreate$',login_required(ProductItemCreate_deprecate.as_view([ProductItemForm_wiard1, ProductItemForm_wiard2])), name='productitem_create_test'),
    url(r'^$',login_required(ProductItemCreate.as_view()), name='productitem_create'),
)