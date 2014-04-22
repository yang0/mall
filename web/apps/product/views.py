#_*_coding:utf-8_*_

import logging
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .models import ProductItem
from .form import ProductItemForm
from django.http import HttpResponse
from apps.common.base import BaseCreateView
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from apps.product.form import ProductItemForm_wiard1



class ProductItemListView(ListView):
    """"""
    model = ProductItem
    context_object_name="productitemList"


    def get_queryset(self):
        querySet = super(ProductItemListView, self).get_queryset()
        return querySet


    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        return context


class ProductItemDetailView(DetailView):
    model = ProductItem
    context_object_name="productitem"



class ProductItemCreate(FormView):
    model = ProductItem
    form_class = ProductItemForm
    template_name = 'product/productItem_form.html'




TEMPLATES = {"0": "product/productItem_form_1.html",
             "1": "product/productItem_form_2.html",}
class ProductItemCreate_deprecate(SessionWizardView):
    #deprecate 基于formwizard的方式添加商品，暂时弃用，仅供以后编码参考

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]


    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/')


    def get_context_data(self, form, **kwargs):
        context = super(ProductItemCreate, self).get_context_data(form=form, **kwargs)
        if self.steps.current == '1':
            data = self.get_cleaned_data_for_step('0')
            context.update({'categoryId': data["product_category"].id})
        return context
