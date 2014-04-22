#_*_coding:utf-8_*_

from .models import Pic
from .serializer import PicSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from apps.user.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.common.api_permission import OwnerPermissions

class PicApi(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
	#只有登录后才能使用
    permission_classes = (IsAuthenticated,OwnerPermissions, )
    serializer_class = PicSerializer
    model = Pic




class PicList(generics.ListAPIView):
    """ 取得当前用户的所有相关数据，如果根据其他条件来去列表，请自行修改 """
    #只有登录后才能使用
    permission_classes = (IsAuthenticated,)
    serializer_class = PicSerializer
    model = Pic

    def get_queryset(self):
    	return Pic.objects.all().filter(user=self.request.user)