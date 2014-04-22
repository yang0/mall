#_*_coding:utf-8_*_

from .models import EavProp
from .serializer import EavPropSerializer, EavEnumGroupSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.common.api_permission import AdminPermissions
from .eav_models import EavEnumGroup

class EavPropApi(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
	#只有登录后才能使用
    permission_classes = (IsAuthenticated,AdminPermissions)
    serializer_class = EavPropSerializer
    model = EavProp

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_object(self):
    	""" 取得当前用户下的记录，和通常的需求不符，如果要根据主键来查询，删掉本方法即可 """
    	queryset = self.get_queryset()
    	filter={'user':self.request.user}
    	return get_object_or_404(queryset, **filter)


class EavPropList(generics.ListAPIView):
    """ 取得当前用户的所有相关数据，如果根据其他条件来去列表，请自行修改 """
    #只有登录后才能使用
    permission_classes = (IsAuthenticated,AdminPermissions)
    serializer_class = EavPropSerializer
    model = EavProp

    def get_queryset(self):
    	return EavProp.objects.all().filter(user=self.request.user)


class EavEnumGroupApi(generics.RetrieveAPIView):
    """获取枚举值分组及其下的所有枚举值"""
    permission_classes = (IsAuthenticated,AdminPermissions)
    serializer_class = EavEnumGroupSerializer
    model = EavEnumGroup


        