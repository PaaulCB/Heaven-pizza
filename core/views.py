from django.shortcuts import render
def home(request):
    """
    This view loads the home(index) template
    """
    return render(request, "core/index.html")