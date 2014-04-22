from .models import Room
from django.contrib import admin


class RoomAdmin(admin.ModelAdmin):
	#list_display = ('email', 'nick', 'create_time')
	model = Room
	#search_fields=['email','nick']
	#list_filter = ('is_staff', 'role_id')
	#date_hierarchy = 'create_time'

admin.site.register(Room, RoomAdmin)