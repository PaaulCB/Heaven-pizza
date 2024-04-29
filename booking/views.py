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
# Constant to store the interval between bookings(used to find alternatives)
BOOKING_INTERVAL = timedelta(minutes=30)
@login_required
def FindBooking(request):
    """
    This view checks if there its a booking available with the data provided by the user.
    If its not give him alternatives times for the booking.
    """
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
    """
    This view creates the Booking and BookingTime instances on the database
    If the user needs to book more than a table create multiple BookingTime instances
    with the same Booking id
    """
    if request.method == "POST":
        #Get the data
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
    """
    Function the  check if there are any available table at the time provided
    for the number of guest provided.
    Returns [] if not available
    """
    # Gets all the tables
    all_tables = Table.objects.all()
    available_tables = []
    # Iterate through the tables
    for table in all_tables:
        # If dont find any bookingTime where the table=table, 
        # the start_time its greater than or equal to the date-BOOKING_DURATION,
        # and the end_time its lesser than or equal to the date+BOOKING_DURATION 
        # Excluding the ones where the booking_id = booking_id provided
        if not BookingTime.objects.exclude(
                booking__booking_id=booking_id
            ).filter(
                table=table,
                start_time__gte=booking_datetime - BOOKING_DURATION,
                start_time__lte=booking_datetime + BOOKING_DURATION
            ).exists():
            # Append it to available_tables
            available_tables.append(table)

    booking_tables = []
    capacity_count = 0
    guests=int(guests)
    # Iterate through available tables
    for table in available_tables:
        booking_tables.append(table)
        capacity_count += table.capacity
        if capacity_count >= guests:
            # If there are enough tables availables to fit the number of guest then return booking_tables
            return booking_tables
    return [] # Otherwise return []

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
                # If finds enough tables to reach the number of guests appends the table ids and the time
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
    """
    View to show the booking of the user.
    login_requiered its used to ensure that the user its logged in
    return the bookings splited in active and past bookings
    """
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
    """
    View to delete a booking
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.user == request.user:
        booking.delete()
        messages.add_message(request, messages.SUCCESS, 'Booking deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own bookings!') 
    
    return redirect('my_bookings')

def modify_booking(request, booking_id):
    """
    View to modify a booking
    """
    booking = get_object_or_404(Booking, pk=booking_id) # Gets the booking
    data = get_data(request) # Gets the data
    if booking.user == request.user:
        booking.date = data['booking_datetime']
        booking.child_chair = data['child_chair']
        booking.allergies = data['allergies']
        booking.number_of_guests = data['number_of_guests']
        booking.booking_name = data['booking_name']
        booking.table_preferences = data['table_preferences']
        #Delete the outdated BookingTime instances
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
    """
    Function to get the data
    """
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
    # Set the data
    data = {
    'number_of_guests': number_of_guests,
    'child_chair': child_chair,
    'allergies': allergies,
    'booking_name': booking_name,
    'table_preferences': table_preferences,
    'booking_datetime': booking_datetime,
    'table_id': table_id
    }
    return data # Return the data