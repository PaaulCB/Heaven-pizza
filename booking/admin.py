from django.contrib import admin
from .models import Booking, Table, BookingTime
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
admin.site.register(Table)
@admin.register(Booking)
class BookingAdmin(SummernoteModelAdmin):
    list_display = ('user','booking_id')
    search_fields = ['user']
    list_filter = ('user','date')
@admin.register(BookingTime)
class BookingAdmin(SummernoteModelAdmin):
    list_display = ('booking','table', 'start_time', 'end_time')
    search_fields = ['table']
    list_filter = ('table','start_time')