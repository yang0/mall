from .models import {{ modelClazz }}
from django.contrib import admin


class {{ modelClazz }}Admin(admin.ModelAdmin):
	#list_display = ('email', 'nick', 'create_time')
	model = {{ modelClazz }}
	#search_fields=['email','nick']
	#list_filter = ('is_staff', 'role_id')
	#date_hierarchy = 'create_time'

admin.site.register({{ modelClazz }}, {{ modelClazz }}Admin)