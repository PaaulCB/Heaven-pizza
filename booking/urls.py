from . import views
from django.urls import path

urlpatterns = [
    path('', views.BookingForm, name='booking'),
    path('booking-confirmation/', views.FindBooking, name='FindBooking'),
]