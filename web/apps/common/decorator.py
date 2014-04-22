#_*_coding:utf-8_*_

try:
    from urllib.parse import urlparse
except ImportError:     # Python 2
    from urlparse import urlparse
import logging
from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.utils.encoding import force_str
from django.shortcuts import resolve_url
from apps.common.role import *
logger = logging.getLogger('django.request')

# def role_required(role_list,redirect_field_name=REDIRECT_FIELD_NAME):
#     def decorator(func):
#         @wraps(func) 
#         def role_right(request,*args,**kwargs):
#             if not request.user.is_authenticated() or not request.user.role_id in role_list:
#                 path = request.build_absolute_uri()
#                 # urlparse chokes on lazy objects in Python 3, force to str
#                 resolved_login_url = force_str(
#                     resolve_url(settings.LOGIN_URL))
#                 # If the login url is the same scheme and net location then just
#                 # use the path as the "next" url.
#                 login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
#                 current_scheme, current_netloc = urlparse(path)[:2]
#                 if ((not login_scheme or login_scheme == current_scheme) and
#                     (not login_netloc or login_netloc == current_netloc)):
#                     path = request.get_full_path()
#                 from django.contrib.auth.views import redirect_to_login
#                 return redirect_to_login(
#                     path, resolved_login_url, redirect_field_name)
  
#             return func(request,*args,**kwargs)
#         return role_right
#     return decorator



# def role_required(role_list,function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
#     """
#     判断是否为管理员或者运营
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_authenticated() and (u.role_id in role_list),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator

def stuff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    判断是否为管理员或者运营
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and (u.is_admin() or u.is_operator()),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    判断是否为管理员
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and (u.is_admin()),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def designer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    判断是否为管理员
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and (u.is_designer()),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator