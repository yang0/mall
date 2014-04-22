#_*_coding:utf-8_*_

from rest_framework import serializers
from .models import EavProp
from .eav_models import EavEnumGroup, EavEnumValue

class EavPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = EavProp
        exclude = ('user','create_time', 'update_time', 'description')


class EavEnumValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EavEnumValue
        exclude = ('create_time', 'eav_enum_group')



class EavEnumGroupSerializer(serializers.ModelSerializer):
    eavEnumValues = EavEnumValueSerializer(many=True)

    class Meta:
        model = EavEnumGroup