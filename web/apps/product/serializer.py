#_*_coding:utf-8_*_

from rest_framework import serializers
from .models import ProductItem, ProductCategoryProp,ProductCategory
from apps.eav.serializer import EavPropSerializer


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        #exclude = ('user',)


class ProductCategorySerializer(serializers.ModelSerializer):
    props = EavPropSerializer(many=True, read_only = True)

    class Meta:
        model = ProductCategory


class ProductCategoryPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryProp