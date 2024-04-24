from . import views
from django.urls import path

urlpatterns = [
    path('', views.FindBooking, name='booking_form'),
    path('booking-confirmation/', views.make_booking, name='make_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]