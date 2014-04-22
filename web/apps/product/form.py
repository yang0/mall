# encoding: utf-8

from django.forms import Textarea, TextInput, FileInput,HiddenInput,NumberInput
from .models import ProductItem, ProductCategory
from django import forms
#from apps.area.widgets import CitySelect, NewSelect
from django.forms import Select
from apps.common.base import BaseForm
from mptt.forms import TreeNodeChoiceField
from apps.area.models import City

"""
class ProductItemForm(BaseForm):
    product_category = TreeNodeChoiceField(queryset=ProductCategory.objects.all(), label=u'商品分类', level_indicator=u'|--')

    class Meta:
    	model = ProductItem
    	exclude = ["user"]
        
        widgets = {
        	'description':Textarea(attrs={'rows': 5,  'style':'width:300px;'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductItemForm, self).__init__(*args, **kwargs)
"""


class ProductItemForm(BaseForm):
    product_category = TreeNodeChoiceField(queryset=ProductCategory.objects.all(), label=u'商品分类', level_indicator=u'|--')
    modelName = "productItem"

    class Meta:
        model = ProductItem
        fields = ["product_category"]
        

    def __init__(self, *args, **kwargs):
        super(ProductItemForm, self).__init__(*args, **kwargs)


class ProductItemForm_wiard1(BaseForm):
    product_category = TreeNodeChoiceField(queryset=ProductCategory.objects.all(), label=u'商品分类', level_indicator=u'|--')
    modelName = "productItem"

    class Meta:
    	model = ProductItem
    	fields = ["product_category"]
        

    def __init__(self, *args, **kwargs):
        super(ProductItemForm_wiard1, self).__init__(*args, **kwargs)
        


class ProductItemForm_wiard2(BaseForm):
    city = TreeNodeChoiceField(queryset=City.objects.filter(level__lt=2), label=u'商品所在城市', level_indicator=u'|--')
    modelName = "productItem"

    class Meta:
    	model = ProductItem
    	exclude = ["product_category", "user", "state"]
        

    def __init__(self, *args, **kwargs):
        super(ProductItemForm_wiard2, self).__init__(*args, **kwargs)

