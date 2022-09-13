from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

# path('api/', include(router.urls))のための設定
from .views import TemplateViewSet
router = routers.DefaultRouter()
router.register('template', views.TemplateViewSet)

app_name = "Restapp"

urlpatterns = [
    path('index/', views.index, name='index'),
    path('api/', include(router.urls)),
    path('nonseializers_api/', views.NonSeializers_Api.as_view(), name = "NonSeializers_Api"),
]