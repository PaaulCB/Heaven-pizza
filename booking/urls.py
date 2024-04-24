from . import views
from django.urls import path

urlpatterns = [
    path('', views.FindBooking, name='booking_form'),
    path('booking-confirmation/', views.make_booking, name='make_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-bookings/delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('my-bookings/modify_booking/<int:booking_id>/', views.modify_booking, name='modify_booking'),
]