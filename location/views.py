from django.shortcuts import render


def ViewLocation(request):
    """
    This view loads the location template
    """
    return render(request, 'location/location.html')
