from django.urls import path

from . import views

urlpatterns = [
    path('', views.classroom_list, name='list'),
    path('<slug:slug>/', views.classroom_detail, name='detail'),
    path('<slug:slug>/enroll/', views.classroom_enroll, name='enroll'),
]
