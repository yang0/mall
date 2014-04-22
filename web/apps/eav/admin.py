#_*_coding:utf-8_*_

from .eav_models import EavProp, EavEnumGroup, EavEnumValue
from .models import  ProductSellPropGroup, ProductSellPropValue, EavValue
from django.contrib import admin


class EavPropAdmin(admin.ModelAdmin):
	list_display = ('name', 'datatype', 'create_time')
	model = EavProp
	#search_fields=['email','nick']
	list_filter = ('datatype', 'prop_type')
	#date_hierarchy = 'create_time'

	def save_model(self, request, obj, form, change):
		obj.creator = request.user
		super(EavPropAdmin, self).save_model(request, obj, form, change)

admin.site.register(EavProp, EavPropAdmin)



class EavEnumGroupAdmin(admin.ModelAdmin):
	list_display = ('name', )
	model = EavEnumGroup
	#search_fields=['email','nick']
	#list_filter = ('datatype', 'prop_type')
	#date_hierarchy = 'create_time'

admin.site.register(EavEnumGroup, EavEnumGroupAdmin)


class EavValueAdmin(admin.ModelAdmin):
	list_display = ('eav_prop', 'product_item')
	model = EavValue
	#search_fields=['email','nick']
	#list_filter = ('datatype', 'prop_type')
	#date_hierarchy = 'create_time'

admin.site.register(EavValue, EavValueAdmin)



class EavEnumValueAdmin(admin.ModelAdmin):
	list_display = ('value','eav_enum_group', 'create_time')
	model = EavEnumValue

admin.site.register(EavEnumValue, EavEnumValueAdmin)


class ProductSellPropGroupAdmin(admin.ModelAdmin):
	list_display = ('name','product_item', 'create_time')
	model = ProductSellPropGroup

admin.site.register(ProductSellPropGroup, ProductSellPropGroupAdmin)


class ProductSellPropValueAdmin(admin.ModelAdmin):
	list_display = ('product_sell_prop_group','eav_enum_value', 'create_time')
	model = ProductSellPropValue

admin.site.register(ProductSellPropValue, ProductSellPropValueAdmin)

