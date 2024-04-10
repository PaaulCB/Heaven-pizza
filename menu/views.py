from django.shortcuts import render
from django.views import generic
from .models import MenuItem

# Create your views here
class MenuItemList(generic.ListView):
    # View to show the menu items
    queryset = MenuItem.objects.all()
    template_name = "menu.html"