#_*_coding:utf-8_*_

import logging
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import {{ modelClazz }}
from .form import {{ modelClazz }}Form
from django.http import HttpResponse
from apps.common.base import BaseCreateView



class {{ modelClazz }}ListView(ListView):
    """获取本网站的游戏排行榜"""
    model = {{ modelClazz }}
    context_object_name="{{ modelClazz | lower}}List"


    def get_queryset(self):
        querySet = super({{ modelClazz }}ListView, self).get_queryset()
        return querySet


    def get_context_data(self, **kwargs):
        context = super({{ modelClazz }}ListView, self).get_context_data(**kwargs)
        return context







class {{ modelClazz }}DetailView(DetailView):
    model = {{ modelClazz }}
    context_object_name="{{ modelClazz | lower}}"







class {{ modelClazz }}Create(BaseCreateView):
    model = {{ modelClazz }}
    form_class = {{ modelClazz }}Form
    #success_url = '/game/%(pk)/pic/form'

    def form_valid(self, form):
    	{{ modelClazz | lower}} = form.save(commit=False)
    	{{ modelClazz | lower}}.creator = self.request.user
        #{{ modelClazz | lower}}.update_time = datetime.now()
    	return super({{ modelClazz}}Create, self).form_valid(form)

    def get_success_url(self):
    	return reverse("{{ modelClazz | lower}}_update", args=(self.object.id,))
