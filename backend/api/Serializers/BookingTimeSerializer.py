from rest_framework import serializers
from api.models import Booking_time


class BookingTimeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Booking_time
    fields = ("id", "availability_date", "user", "package", "client_description", "email", "phonenumber", "location", "is_booked")