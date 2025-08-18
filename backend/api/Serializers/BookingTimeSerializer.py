from rest_framework import serializers
from api.models import Booking_time


class BookingTimeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Booking_time
    fields = ("id", "availability_date", "name", "user", "package", "client_description", "email", "phone_number", "location", "is_booked")