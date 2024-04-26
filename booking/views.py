from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import make_aware
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import Table, BookingTime, Booking
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Constant to store the duration of the booking
BOOKING_DURATION = timedelta(hours=1)
BOOKING_INTERVAL = timedelta(minutes=30)
@login_required
def FindBooking(request):
    if request.method == 'POST':
        # Get date and time
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        booking_id = request.POST.get('booking_id')
        guests = request.POST.get('number_of_guests')
        booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", "%Y-%m-%d %H:%M")
        # Make datetime aware
        aware_booking_datetime = make_aware(booking_datetime)
        # Find availables tables
        available_tables = find_available_tables(aware_booking_datetime, guests, int(booking_id))
        if available_tables:
            table_ids = [str(table.table_id) for table in available_tables]
            join_table_id='-'.join(table_ids)
            return JsonResponse({'available': True, 'table_id':join_table_id})
        else:
            alternatives = find_alternatives(aware_booking_datetime, guests, int(booking_id))
            return JsonResponse({'available': False, 'alternatives': alternatives})

    else:
        return render(request, 'booking/booking.html')

def make_booking(request):
    if request.method == "POST":
        #Get the data from the form
        data = get_data(request)
        #Booking instance
        booking = Booking(
            date = data['booking_datetime'],
            user = request.user, 
            number_of_guests = data['number_of_guests'], 
            child_chair = data['child_chair'], 
            allergies = data['allergies'],
            booking_name = data['booking_name'],
            table_preferences = data['table_preferences'])
        booking.save()
        #Set start and end time
        start_time = data['booking_datetime']
        end_time = start_time + BOOKING_DURATION
        # Split the tables ids
        table_ids = data['table_id'].split('-')
        for table_id in table_ids:
            # Get tables
            table = get_object_or_404(Table, table_id=table_id)
            #BookingTime instance
            booking_time = BookingTime(booking = booking, table = table, start_time = start_time, end_time = end_time)
            booking_time.save()

        messages.add_message(request, messages.SUCCESS, 'Booking created!')
    return redirect('booking_form')

def find_available_tables(booking_datetime, guests, booking_id):
    all_tables = Table.objects.all()
    available_tables = []
    for table in all_tables:
        if not BookingTime.objects.exclude(
                booking__booking_id=booking_id
            ).filter(
                table=table,
                start_time__gte=booking_datetime - BOOKING_DURATION,
                start_time__lte=booking_datetime + BOOKING_DURATION
            ).exists():
            available_tables.append(table)

    booking_tables = []
    capacity_count = 0
    guests=int(guests)
    for table in available_tables:
        booking_tables.append(table)
        capacity_count += table.capacity
        if capacity_count >= guests:
            return booking_tables
    return []

def find_alternatives(booking_datetime, guests, booking_id):

    alternatives = []
    guests = int(guests)
    current_datetime = booking_datetime
        
    # While loop to find 3 alternatives
    while len(alternatives) < 3:
        available_tables = []
        capacity_count = 0
        # Iterate through the tables to check if there any available table at that time
        for table in Table.objects.all():
            if not BookingTime.objects.exclude(
                booking__booking_id=booking_id
            ).filter(
                table=table,
                start_time__gte=current_datetime - BOOKING_DURATION,
                start_time__lte=current_datetime + BOOKING_DURATION
            ).exists():
                available_tables.append(table)
                capacity_count+=table.capacity
                # If finds enough tables to reach the number of guests ppends the table ids and the time
                if capacity_count >= guests:
                    alternatives.append({
                        'table_id': '-'.join(str(table.table_id) for table in available_tables),
                        'time': current_datetime
                    })
                    # break the loop
                    break
            
        # Increment the time for the next iteration
        current_datetime += BOOKING_INTERVAL
        
    return alternatives

@login_required
def my_bookings(request):
    # Get the current time
    current_time = timezone.now()
    # Get the active bookings of the user
    active_bookings = Booking.objects.filter(user=request.user, date__gt=current_time).order_by('date')
    # Get the past bookings of the user
    past_bookings = Booking.objects.filter(user=request.user, date__lte=current_time).order_by('-date')
    return render(request, 'booking/my_bookings.html', {
        'active_bookings': active_bookings,
        'past_bookings': past_bookings
    })

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.user == request.user:
        booking.delete()
        messages.add_message(request, messages.SUCCESS, 'Booking deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own bookings!') 
    
    return redirect('my_bookings')

def modify_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    data = get_data(request)
    if booking.user == request.user:
        booking.date = data['booking_datetime']
        booking.child_chair = data['child_chair']
        booking.allergies = data['allergies']
        booking.number_of_guests = data['number_of_guests']
        booking.booking_name = data['booking_name']
        booking.table_preferences = data['table_preferences']
        #Delete the outdated bookingtime instances
        BookingTime.objects.filter(booking=booking).delete()
        booking.save()
        #Set start and end time
        start_time = data['booking_datetime']
        end_time = start_time + BOOKING_DURATION
        # Split the tables ids
        table_ids = data['table_id'].split('-')
        for table_id in table_ids:
            # Get tables
            table = get_object_or_404(Table, table_id=table_id)
            #BookingTime instance
            booking_time = BookingTime(booking = booking, table = table, start_time = start_time, end_time = end_time)
            booking_time.save()
        messages.add_message(request, messages.SUCCESS, 'Booking modified!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only modify your own bookings!') 
    return redirect('my_bookings')

def get_data(request):

    number_of_guests = request.POST.get('number_of_guests')
    child_chair = request.POST.get('child_chair') == "on"
    allergies = request.POST.get('allergies')
    booking_name = request.POST.get('booking_name')
    table_preferences = request.POST.get('table_preferences')
    booking_datetime = None
    table_id = None
    # Checks which button was pressed
    button = request.POST.get('form-button')

    # Get the correct datetime and table_id based on the button pressed
    if button in ['make-booking', 'book-option-1', 'book-option-2', 'book-option-3']:
        if button == 'make-booking':
            date = request.POST.get('booking_date') + ' ' + request.POST.get('booking_time')
        else:
            date = request.POST.get(f"{button}-time").rstrip('Z')
            
        # Make aware the datetime
        booking_datetime = make_aware(datetime.strptime(date, '%Y-%m-%d %H:%M') if button == 'make-booking' else datetime.fromisoformat(date))
        table_id = request.POST.get("table_id") if button == 'make-booking' else request.POST.get(f"{button}-table_id")
    data = {
    'number_of_guests': number_of_guests,
    'child_chair': child_chair,
    'allergies': allergies,
    'booking_name': booking_name,
    'table_preferences': table_preferences,
    'booking_datetime': booking_datetime,
    'table_id': table_id
    }
    return data