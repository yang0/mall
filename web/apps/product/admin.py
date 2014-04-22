#_*_coding:utf-8_*_

from .models import ProductItem, Brand, ProductCategory, ProductCategoryProp, ProductSku, ProductSkuValue
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

import sys 

reload(sys) 
sys.setdefaultencoding("utf-8") 



class ProductItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'brand', 'create_time')
	model = ProductItem
	search_fields=['title','description']
	list_filter = ('brand__name', )
	date_hierarchy = 'create_time'

	def save_model(self, request, obj, form, change):
		obj.creator = request.user
		super(ProductItemAdmin, self).save_model(request, obj, form, change)

admin.site.register(ProductItem, ProductItemAdmin)




class BrandAdmin(admin.ModelAdmin):
	list_display = ('name',)
	model = Brand
	#search_fields=['email','nick']
	#list_filter = ('is_staff', 'role_id')
	#date_hierarchy = 'create_time'

admin.site.register(Brand, BrandAdmin)




admin.site.register(ProductCategory, MPTTModelAdmin)




class ProductCategoryPropAdmin(admin.ModelAdmin):
	list_display = ('product_category','eav_prop', 'create_time')
	model = ProductCategoryProp
	#search_fields=['email','nick']
	list_filter = ('product_category__name', )
	#date_hierarchy = 'create_time'

admin.site.register(ProductCategoryProp, ProductCategoryPropAdmin)


class ProductSkuAdmin(admin.ModelAdmin):
	list_display = ('product_item','price', 'num', 'sold_num', 'create_time')
	model = ProductSku
	#search_fields=['email','nick']
	#list_filter = ('product_category__name', )
	#date_hierarchy = 'create_time'

admin.site.register(ProductSku, ProductSkuAdmin)



class ProductSkuValueAdmin(admin.ModelAdmin):
	list_display = ('product_sku','eav_value', 'eav_enum_value',  'create_time')
	model = ProductSkuValue
	#search_fields=['email','nick']
	#list_filter = ('product_category__name', )
	#date_hierarchy = 'create_time'

admin.site.register(ProductSkuValue, ProductSkuValueAdmin)
