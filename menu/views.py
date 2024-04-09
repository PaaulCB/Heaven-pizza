from django.shortcuts import render

# Create your views here.
def view_menu(request):
    return render(request, "menu/menu.html")