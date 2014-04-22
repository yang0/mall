# encoding: utf-8

from django.forms import Textarea, TextInput, FileInput,HiddenInput,NumberInput
from .models import EavProp
from django import forms
#from apps.area.widgets import CitySelect, NewSelect
from django.forms import Select
from apps.common.base import BaseForm


class EavPropForm(BaseForm):

    class Meta:
    	model = EavProp
    	exclude = ["user"]
        
        widgets = {
        	'description':Textarea(attrs={'rows': 5,  'style':'width:300px;'})
        }

    def __init__(self, *args, **kwargs):
        super(EavPropForm, self).__init__(*args, **kwargs)
        

