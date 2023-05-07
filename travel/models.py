
from sqlite3 import Timestamp
from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime

from traitlets import default

class User(AbstractUser):
    phone = models.CharField(max_length = 32, default="None")
    nationality = models.CharField(max_length = 32, default="None")

class Airport(models.Model):
    name = models.CharField(max_length = 128, default = "none")
    iataCode = models.CharField(max_length = 4)
    city = models.CharField(max_length = 32, default= "none")
    country = models.CharField(max_length=32, default="none")

class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="origin")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination")
    departure_date = models.CharField(max_length = 32 )
    arrival_date = models.CharField(max_length = 32 )
    airline = models.CharField(max_length = 128, default="none")
    plane = models.CharField(max_length = 128, default="none")
    duration = models.CharField(max_length = 16)
   

class Booking(models.Model):
    id = models.AutoField(primary_key = True)
    pnr_number = models.CharField(max_length=6, unique=True, null=True, default=None)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    flights = models.ManyToManyField(Flight, related_name = "flights", blank=True)
    booking_time = models.DateTimeField()
    














""" class arrival:
    iataCode

class Segment:
    departure
    arrival
    duration

class Itinerary:
    segment = models.ManyToManyField(Segment)    

class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    Itinerary = models.ManyToManyField(Itinerary)
     """