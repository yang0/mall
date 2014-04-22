#_*_coding:utf-8_*_


from django.db import models

from apps.common.common import get_file_path


class Room(models.Model):
    name = models.CharField(u'空间名称', max_length=10L)

    class Meta:
        db_table = 'room'
        verbose_name = verbose_name_plural = u'room'


    def __unicode__(self):
        return self.name
