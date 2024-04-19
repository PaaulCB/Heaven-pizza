from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_guests = models.PositiveIntegerField()
    child_chair = models.BooleanField(default=False)
    allergies = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"ID: {self.booking_id} | by {self.user} | Date: { self.date}"

class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"ID: {self.table_id} | Capacity: {self.capacity}"

class BookingTime(models.Model):
    booking_time_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Booking: {self.booking} | Table: {self.table} | Date: { self.start_time}"