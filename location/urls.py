from . import views
from django.urls import path

urlpatterns = [
    path('', views.ViewLocation, name='location'),
]