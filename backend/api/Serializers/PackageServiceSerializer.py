from rest_framework import serializers
from api.models import Package_Service

class PackageServiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Package_Service
    fields = ("id", "services", "package")