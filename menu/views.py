from django.shortcuts import render
from .models import MenuItem

# Create your views here
def MenuItemList(request):
    # Gets all the items form the menu
    queryset = MenuItem.objects.all()
    # Gets the distincts types of the items.
    types = MenuItem.objects.values_list('type', flat=True).distinct()
    return render(request, 'menu/menuitem_list.html', {'types': types , 'items':queryset})