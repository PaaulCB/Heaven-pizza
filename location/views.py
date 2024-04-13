from django.shortcuts import render
# Create your views here.
def ViewLocation(request):
    
    return render(request,'location/location.html')