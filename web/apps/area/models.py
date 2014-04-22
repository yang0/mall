#_*_coding:utf-8_*_

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class City(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


    class Meta:
        db_table = 'city'
        verbose_name = verbose_name_plural = (u'城市')

    def __unicode__(self):
        return self.name


