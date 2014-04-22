#_*_coding:utf-8_*_

import logging
from apps.area.models import City, School
from apps.common.mixin import JSONResponseMixin
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core import serializers
from rest_framework import generics
from .serializer import SchoolSerializer
from django.db.models import Q


logger = logging.getLogger(__name__)

class CityChildren(JSONResponseMixin, ListView):
	"""城市的直接下属节点"""
	model = City

	def get_queryset(self):
		parentId = '0'
		parentId = self.kwargs['parentId']
		if parentId == '0':
			return City.objects.filter(level=0).order_by("id").values("id", "name", "parent", "level")
		
		return City.objects.filter(parent_id=parentId).order_by("id").values("id", "name", "parent", "level")


class CityAncestors(JSONResponseMixin, ListView):
	"""城市的直接上级节点,包含自己"""
	model = City

	def get_queryset(self):
		cityId = '0'
		cityId = self.kwargs['cityId']
		city = City.objects.filter(pk=cityId)
		if len(city) == 0:
			return
		
		return city[0].get_ancestors(False, True).values("id","name","parent", "level")


class CityDetail(JSONResponseMixin, DetailView):
	""" 取得城市信息 """
	model = City



class CityDescendants(JSONResponseMixin, ListView):
	""" 城市的所有下属节点，不包含自己 """
	model = City

	def get_queryset(self):
		parentId = 0
		parentId = self.kwargs['parentId']
		city = City.objects.filter(pk=parentId)
		if len(city) == 0:
			return

		return city[0].get_descendants(False).values("id","name","parent", "level")



