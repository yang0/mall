#_*_coding:utf-8_*_

import logging
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Room
from .form import RoomForm
from django.http import HttpResponse
from apps.common.base import BaseCreateView



class RoomListView(ListView):
    """获取本网站的游戏排行榜"""
    model = Room
    context_object_name="roomList"


    def get_queryset(self):
        querySet = super(RoomListView, self).get_queryset()
        return querySet


    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        return context







class RoomDetailView(DetailView):
    model = Room
    context_object_name="room"







class RoomCreate(BaseCreateView):
    model = Room
    form_class = RoomForm
    #success_url = '/game/%(pk)/pic/form'

    def form_valid(self, form):
    	room = form.save(commit=False)
    	room.creator = self.request.user
        #room.update_time = datetime.now()
    	return super(RoomCreate, self).form_valid(form)

    def get_success_url(self):
    	return reverse("room_update", args=(self.object.id,))
