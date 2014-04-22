#_*_coding:utf-8_*_


from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from apps.common.common import get_file_path


class Pic(models.Model):
    object_id = models.PositiveIntegerField(verbose_name=u'对象id')
    content_type = models.ForeignKey(ContentType, verbose_name=u'对象类型', editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    pic = models.ImageField(u'图片路径', upload_to=get_file_path)
    description = models.CharField(u'图片描述', max_length=5000L,blank=True)
    creator = models.ForeignKey(User, editable=False, verbose_name=u'')
    create_time = models.DateTimeField(u'', auto_now_add=True)
    update_time = models.DateTimeField(u'', auto_now=True)

    class Meta:
        db_table = 'pic'
        verbose_name = verbose_name_plural = u'图片'


    def __unicode__(self):
        return self.pic
