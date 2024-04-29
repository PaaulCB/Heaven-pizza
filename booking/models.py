from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    """
    Model that store related to the booking such as date,user, number_of_guests,
    child_chair, allergies, booking_name and table_preferencies
    """
    booking_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_guests = models.PositiveIntegerField()
    child_chair = models.BooleanField(default=False)
    allergies = models.TextField(blank=True, null=True)
    booking_name = models.CharField(max_length=50, blank=True, null=True)
    table_preferences = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"ID: {self.booking_id}"

class Table(models.Model):
    """
    Modal to store the tables along with it capacity 
    Need to be added by an admin using the admin panel
    The tables are not intented to be changed so if need any change needs to do it manually
    using the admin panel.
    """
    table_id = models.AutoField(primary_key=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"ID: {self.table_id} | Capacity: {self.capacity}"

class BookingTime(models.Model):
    """
    Modal to store data and the ralation between Booking and table
    have booking and table as foreign key.
    start_time and end_time store as it name says,
    the starting and ending time of the booking on that specific table
    """
    booking_time_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Booking: {self.booking} | Table: {self.table} | Date: { self.start_time}"