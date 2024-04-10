from . import views
from django.urls import path

urlpatterns = [
    path('', views.MenuItemList.as_view(), name='menu'),
]