from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('booking/', include("booking.urls"), name="booking-urls"),
    path("location/", include("location.urls"), name="location-urls"),
    path("menu/", include("menu.urls"), name="menu-urls"),
    path('summernote/', include('django_summernote.urls')),
    path('', home, name='home'),
]
