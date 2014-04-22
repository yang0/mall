#_*_coding:utf-8_*_


from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class EavEnumGroup(models.Model):
    name = models.CharField(u'枚举分组名称', max_length=10L)

    class Meta:
        db_table = 'eav_enum_group'
        verbose_name = verbose_name_plural = u'动态属性--枚举值分组'


    def __unicode__(self):
        return self.name



class EavProp(models.Model):
    DATA_TYPE_CHOICES = (
        (0, u'int'),
        (1, u'flot'),
        (2, u'text'),
        (3, u'date'),
        (4, u'bool'),
        (5, u'枚举'),
    )
    PROP_TYPE_CHOICES = (
        (1, u'关键属性'),
        (2, u'非关键属性'),
        (3, u'销售属性'),
    )
    name = models.CharField(u'属性名称', max_length=10L)
    description = models.CharField(u'描述', max_length=50L)
    eav_group = models.ForeignKey(EavEnumGroup, verbose_name=u'属性关联的enumgroup', null=True, blank=True)
    datatype = models.IntegerField(u'数据类型', choices=DATA_TYPE_CHOICES)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    creator = models.ForeignKey(User, editable=False, verbose_name=u'')
    prop_type = models.IntegerField(u'类型', choices=PROP_TYPE_CHOICES)
    required = models.BooleanField(u'是否必填')

    class Meta:
        db_table = 'eav_prop'
        verbose_name = verbose_name_plural = u'动态属性定义'


    def __unicode__(self):
        return self.name


class EavEnumValue(models.Model):
    value = models.CharField(u'自定义枚举值', max_length=50L)
    eav_enum_group = models.ForeignKey(EavEnumGroup, verbose_name=u'枚举分组', related_name="eavEnumValues")
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        db_table = 'eav_enum_value'
        verbose_name = verbose_name_plural = u'动态属性--枚举值'


    def __unicode__(self):
        return self.value