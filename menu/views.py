from django.shortcuts import render
from .models import MenuItem

# Create your views here
def MenuItemList(request):
    """
    This view return all the items form the menu and all the distinct types of items on the menu. 
    """
    # Gets all the items from the menu
    queryset = MenuItem.objects.all()
    # Gets the distincts types of items.
    types = MenuItem.objects.values_list('type', flat=True).distinct()
    return render(request, 'menu/menuitem_list.html', {'types': types , 'items':queryset})