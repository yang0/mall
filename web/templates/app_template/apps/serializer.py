#_*_coding:utf-8_*_

from rest_framework import serializers
from .models import {{ modelClazz }}

class {{ modelClazz }}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{ modelClazz }}
        exclude = ('user',)