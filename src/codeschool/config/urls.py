import os

from django.urls import path, include
from django.contrib import admin
from boogie.rest import rest_api
from django.contrib.auth import get_user_model

from . import settings

rest_api()(get_user_model())


# Basic URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(rest_api.urls)),

    # Codeschool apps
    path('classrooms/', include('cs_classroom.classrooms.urls')),

    # path('', index_view),
    # url(r'^profile/$', profile_view, name='profile-view'),
    # url(r'^auth/', include('codeschool.accounts.urls', namespace='auth')),
]

# Optional debug views
# if settings.CODESCHOOL_DEBUG_VIEWS or settings.DEBUG:
#     import django.contrib.admin
#
#     urlpatterns += [
#         url(r'^_admin/', django.contrib.admin.site.urls),
#         url(r'^_debug/', include('codeschool.core.urls')),
#     ]

# # Optional "social" urls
# if 'codeschool.social' in settings.INSTALLED_APPS:
#     urlpatterns += [
#         url(r'^social/', include('codeschool.social.urls', namespace='social')),
#     ]

# # Global questions list
# if settings.CODESCHOOL_GLOBAL_QUESTIONS:
#     from codeschool.lms.activities.views import main_question_list
#
#     urlpatterns += [
#         url(r'^questions/$', main_question_list, name='question-list'),
#     ]

# # Courses interface
# if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
#     from codeschool.lms.courses.views import course_list
#
#     urlpatterns += [
#         url(r'^courses/$', course_list, name='course-list'),
#     ]

# # Optional cli/clt interface
# if 'codeschool.cli' in settings.INSTALLED_APPS:
#     from codeschool.cli import api as jsonrpc_api
#
#     urlpatterns += [
#         url(r'^cli/jsonrpc/', include(jsonrpc_api.urls)),
#     ]

# # Wagtail endpoint (these must come last)
# urlpatterns += [
#     wagtail_urls.urlpatterns[0],
#     url(r'^((?:[\w\-\.]+/)*)$',
#         wagtail_urls.views.serve, name='wagtail_serve'),
#     url(r'^((?:[\w\-\.]+/)*[\w\-\.]+\.(?:srvice|json|api)/?)$',
#         wagtail_urls.views.serve, name='wagtail-api-serve'),
# ]

# Django serves static urls for the dev server.
# Production relies on Nginx.
if os.environ.get('DJANGO_SERVE_STATIC', False) or settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
