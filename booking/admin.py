from django.contrib import admin
from .models import Booking, Table, BookingTime
# Register your models here.
admin.site.register(Booking)
admin.site.register(Table)
admin.site.register(BookingTime)