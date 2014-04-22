from rest_framework import permissions

class OwnerPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
    	if obj.user:
    		return request.user.id == obj.user.id
    	elif obj.creator:
    		return request.user.id == obj.creator.id
    	else:
    		return False


class AdminPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
    	return request.user.is_superuser