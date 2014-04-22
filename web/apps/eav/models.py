#_*_coding:utf-8_*_


from django.db import models
from datetime import datetime

from apps.common.common import get_file_path
from django.contrib.auth.models import User
from .eav_models import EavEnumValue, EavProp




from apps.product.models import ProductItem
class ProductSellPropGroup(models.Model):
    name = models.CharField(u'分组名称', max_length=15L)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    product_item = models.ForeignKey(ProductItem, verbose_name=u'商品')
    eavEnumValues = models.ManyToManyField(EavEnumValue, through='ProductSellPropValue', verbose_name=u'枚举值')

    class Meta:
        db_table = 'product_sell_prop_group'
        verbose_name = verbose_name_plural = u'销售属性分组定义'


    def __unicode__(self):
        return self.name


class ProductSellPropValue(models.Model):
    product_sell_prop_group = models.ForeignKey(ProductSellPropGroup, verbose_name=u'销售属性分组定义')
    eav_enum_value = models.ForeignKey(EavEnumValue, verbose_name=u'动态属性值')
    create_time = models.DateTimeField(u'', auto_now_add=True)

    class Meta:
        db_table = 'product_sell_prop_value'
        verbose_name = verbose_name_plural = u'商品销售属性'






class EavValue(models.Model):
    eav_prop = models.ForeignKey(EavProp, verbose_name=u'属性')
    product_item = models.ForeignKey(ProductItem, verbose_name=u'商品')
    value_text = models.CharField(u'text', max_length=50L, null=True, blank=True)
    value_float = models.FloatField(u'float', null=True, blank=True)
    value_int = models.IntegerField(u'int', null=True, blank=True)
    value_date = models.DateTimeField(u'date', null=True, blank=True)
    value_bool = models.IntegerField(u'bool', null=True, blank=True)
    value_enum = models.ForeignKey(EavEnumValue, verbose_name=u'枚举值', null=True, blank=True)
    value_sell_prop_group = models.ForeignKey(ProductSellPropGroup, verbose_name=u'枚举组，仅销售属性用到', null=True, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'', auto_now=True)

    class Meta:
        db_table = 'eav_value'
        verbose_name = verbose_name_plural = u'动态属性的值'

    def __unicode__(self):
        return "%s-%s: %s %s %s %s %s %s" % (self.product_item.title, self.eav_prop
            , self.value_text, self.value_float, self.value_int, self.value_date, self.value_enum, self.value_sell_prop_group)
