#_*_coding:utf-8_*_

from .models import {{ modelClazz }}
from .serializer import {{ modelClazz }}Serializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class {{ modelClazz }}Api(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
	#只有登录后才能使用
    permission_classes = (IsAuthenticated,)
    serializer_class = {{ modelClazz }}Serializer
    model = {{ modelClazz }}

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_object(self):
    	""" 取得当前用户下的记录，和通常的需求不符，如果要根据主键来查询，删掉本方法即可 """
    	queryset = self.get_queryset()
    	filter={'user':self.request.user}
    	return get_object_or_404(queryset, **filter)


class {{ modelClazz }}List(generics.ListAPIView):
    """ 取得当前用户的所有相关数据，如果根据其他条件来去列表，请自行修改 """
    #只有登录后才能使用
    permission_classes = (IsAuthenticated,)
    serializer_class = {{ modelClazz }}Serializer
    model = {{ modelClazz }}

    def get_queryset(self):
    	return {{ modelClazz }}.objects.all().filter(user=self.request.user)