#_*_coding:utf-8_*_

import logging
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Pic
from .form import PicForm
from django.http import HttpResponse
from apps.common.base import BaseCreateView
from django.contrib.contenttypes.models import ContentType
from apps.user.models import DesignerVerify




class PicCreate(BaseCreateView):
    """填写基本设计要求"""
    model = Pic
    form_class = PicForm
    #success_url = '/game/%(pk)/pic/form'

    def form_valid(self, form):
        contentType = ContentType.objects.get(model=self.request.POST["content_type"])
        if contentType.model=="user":
            self.user_model(form,contentType)
        else:
            self.other_model(form,contentType)
    	return super(PicCreate, self).form_valid(form)

    def get_success_url(self):
    	return self.request.POST["next"]


    def user_model(self,form,contentType):
        """上传头像"""
        pic = form.save(commit=False)
        obj=None
        try:
            obj=Pic.objects.get(user=self.request.user,content_type=contentType)
        except:
            pass
        if obj:
            pic.id=obj.id
            pic.create_time=obj.create_time
        pic.user = self.request.user
        pic.content_type = contentType
        pic.save()  #为了获取图片上传后的路径
        if 'avatar' in self.request.session:
            # 更新用户session中头像
            self.request.session['avatar']=str(pic.pic)



    def other_model(self,form,contentType):
        pic = form.save(commit=False)
        pic.user = self.request.user
        pic.content_type = contentType
        pic.save()  #为了获取图片上传后的路径
        # 对应的Object的包含图片数+1
        contentObj=contentType.get_object_for_this_type(pk=pic.object_id)
        data={}
        data['pic_num']=contentObj.pic_num+1
        contentType.model_class().objects.filter(pk=pic.object_id).update(**data)
        # 更新设计师的最新项目图片
        if self.request.POST["content_type"].strip() == 'project':
            DesignerVerify.objects.filter(user_id=self.request.user.id).update(**{"project_pic":pic.pic,"update_time":datetime.now()}) 

