from django.shortcuts import render
# Create your views here.
def ViewLocation(request):
    """
    This view loads the location template
    """
    return render(request,'location/location.html')