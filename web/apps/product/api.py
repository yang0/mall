#_*_coding:utf-8_*_

from .models import ProductItem, ProductCategory, ProductCategoryProp
from .serializer import ProductItemSerializer, ProductCategoryPropSerializer, ProductCategorySerializer

from apps.eav.models import EavProp
from apps.eav.serializer import EavPropSerializer

from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.common.api_permission import AdminPermissions

class ProductItemApi(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    #只有登录后才能使用
    permission_classes = (IsAuthenticated, AdminPermissions)
    serializer_class = ProductItemSerializer
    model = ProductItem

    def pre_save(self, obj):
        obj.creator = self.request.user




class ProductItemList(generics.ListAPIView):
    """ 取得当前用户的所有相关数据，如果根据其他条件来去列表，请自行修改 """
    #只有登录后才能使用
    permission_classes = (IsAuthenticated, AdminPermissions)
    serializer_class = ProductItemSerializer
    model = ProductItem

    def get_queryset(self):
    	return ProductItem.objects.all().filter(user=self.request.user)


class CategoryProps(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, AdminPermissions)
    serializer_class = ProductCategorySerializer
    model = ProductCategory




#class ProductCategoryProp(generics.ListAPIView):
    