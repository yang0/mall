# encoding: utf-8

from django.forms import ModelForm, Textarea, TextInput, FileInput,HiddenInput
from django import forms
from django.views.generic.edit import CreateView



class BaseForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        clazzList = ['TextInput', 'Textarea']
        modelName = self.__class__.__name__.lower()[0:1] + self.__class__.__name__[1:-4]
        for name, field in self.fields.items():
            if field.widget.__class__.__name__ in clazzList:
                if hasattr(field, 'max_length'):
                    if field.max_length >= 30:
                        if field.widget.attrs.has_key('class'):
                            field.widget.attrs['class'] += ' span12'
                        else:
                            field.widget.attrs.update({'class':'span12'})


                
                if isinstance(field, forms.IntegerField):
                    field.widget.attrs['type']='number'

            field.widget.attrs['ng-model'] = '%s.%s' % (modelName,name)

            if field.required:
                field.widget.attrs['ng-required'] = 'true'




class BaseCreateView(CreateView):

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context