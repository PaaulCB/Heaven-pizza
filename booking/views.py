from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Table, BookingTime, Booking
from django.contrib import messages
# Constant to store the duration of the booking in hours
BOOKING_DURATION = 1
def BookingForm(request):

    return render(request,'booking/booking.html')


def FindBooking(request):
    if request.method == "POST":
        #Get the data from the form
        number_of_guests = request.POST.get('number_of_guests')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        if request.POST.get('child_chair') == "on":
            child_chair = True
        else:
            child_chair = False
        allergies = request.POST.get('allergies')
        #Convert date and time to datetime
        booking_datetime = datetime.strptime(f'{booking_date} {booking_time}', '%Y-%m-%d %H:%M')
        #Booking instance
        booking = Booking(date = booking_datetime, user = request.user, number_of_guests = number_of_guests, child_chair = child_chair, allergies = allergies)
        booking.save()
        #Get table instance
        table = Table.objects.get(table_id = 1)
        #Set start and end time
        start_time = booking_datetime
        end_time = start_time + timedelta(hours=BOOKING_DURATION)
        #BookingTime instance
        booking_time = BookingTime(booking = booking, table = table, start_time = start_time, end_time = end_time)
        booking_time.save()
        messages.add_message(request, messages.SUCCESS, 'Booking done')
        messages.add_message(request, messages.ERROR, 'Not available')
        return render(request,'booking/booking.html')