from rest_framework import serializers
from api.models import Review

class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ("id", "description", "user", "rating", "package")