#_*_coding:utf-8_*_

import logging
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import EavProp
from .form import EavPropForm
from django.http import HttpResponse
from apps.common.base import BaseCreateView



class EavPropListView(ListView):
    """获取本网站的游戏排行榜"""
    model = EavProp
    context_object_name="eavpropList"


    def get_queryset(self):
        querySet = super(EavPropListView, self).get_queryset()
        return querySet


    def get_context_data(self, **kwargs):
        context = super(EavPropListView, self).get_context_data(**kwargs)
        return context







class EavPropDetailView(DetailView):
    model = EavProp
    context_object_name="eavprop"







class EavPropCreate(BaseCreateView):
    model = EavProp
    form_class = EavPropForm
    #success_url = '/game/%(pk)/pic/form'

    def form_valid(self, form):
    	eavprop = form.save(commit=False)
    	eavprop.creator = self.request.user
        #eavprop.update_time = datetime.now()
    	return super(EavPropCreate, self).form_valid(form)

    def get_success_url(self):
    	return reverse("eavprop_update", args=(self.object.id,))
