from rest_framework.permissions import BasePermission

from .models import *
from .views import *
import re

# https://github.com/HazyResearch/elementary/blob/master/django/resources/views.py


class UserPermissions(BasePermission):
    """
    Custom user permissions. Admin can do everything. POSTS are allowed from anyone.
    """

    def has_permission(self, request, view):
        single_user_regex = r"/api/users/[0-9]+"
        user_regex = r"/api/users"
        profile_regex =  r"/api/profile/"
        if request.user.is_authenticated() and not request.user.is_staff and re.match(profile_regex,request.path):
            all_info = view.queryset
            owner_user_id = request.user.id
            owner_user_info = Profile.objects.filter(id=owner_user_id)
            view.queryset = owner_user_info
            return request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT']
        if request.user.is_authenticated() and not request.user.is_staff:
            all_info = view.queryset
            owner_user_id = request.user.id
            owner_user_info = User.objects.filter(id=owner_user_id)
            view.queryset = owner_user_info
            return request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT']
        if re.match(single_user_regex, request.path):
            url_user_search = re.search(r"[0-9]+", request.path)
            url_user_id = int(url_user_search.group(0))
            return request.user.id == url_user_id or request.user.is_staff
        if not request.user or not request.user.is_authenticated():
            return request.method == 'POST'
        if re.match(user_regex, request.path) or re.match(profile_regex,request.path):
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user == obj
