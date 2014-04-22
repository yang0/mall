#_*_coding:utf-8_*_

from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('user',)