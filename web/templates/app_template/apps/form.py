# encoding: utf-8

from django.forms import Textarea, TextInput, FileInput,HiddenInput,NumberInput
from .models import {{ modelClazz }}
from django import forms
#from apps.area.widgets import CitySelect, NewSelect
from django.forms import Select
from apps.common.base import BaseForm


class {{ modelClazz }}Form(BaseForm):

    class Meta:
    	model = {{ modelClazz }}
    	exclude = ["user"]
        
        widgets = {
        	'description':Textarea(attrs={'rows': 5,  'style':'width:300px;'})
        }

    def __init__(self, *args, **kwargs):
        super({{ modelClazz }}Form, self).__init__(*args, **kwargs)
        

