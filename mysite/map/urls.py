from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'map'

urlpatterns = [
    path('', views.jeju_map, name='jeju_map'),
]