from django.db import models
from django.conf import settings
from .Package import Package


class Booking_time(models.Model):
  availability_date = models.DateTimeField()
  user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
  client_description = models.CharField(max_length=155)
  email = models.CharField(max_length=155)
  phone_number = models.CharField(max_length=20)
  location = models.CharField(max_length=155)
  is_booked = models.BooleanField()

