from django.shortcuts import render
# Create your views here.
def MyBookings(request):
    
    return render(request,'booking/booking.html')