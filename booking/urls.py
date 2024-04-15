from . import views
from django.urls import path

urlpatterns = [
    path('', views.MyBookings, name='booking'),
]