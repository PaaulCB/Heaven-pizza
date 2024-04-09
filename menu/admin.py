from django.contrib import admin
from .models import MenuItem
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(MenuItem)
class MenuItemAdmin(SummernoteModelAdmin):
    list_display = ('name', 'price', 'kcal', 'type', 'badge')
    search_fields = ['name','type','price']
    list_filter = ('type','badge')
    summernote_fields = ('description')