from .models import Pic
from django.contrib import admin


class PicAdmin(admin.ModelAdmin):
	#list_display = ('email', 'nick', 'create_time')
	model = Pic
	#search_fields=['email','nick']
	#list_filter = ('is_staff', 'role_id')
	#date_hierarchy = 'create_time'

admin.site.register(Pic, PicAdmin)