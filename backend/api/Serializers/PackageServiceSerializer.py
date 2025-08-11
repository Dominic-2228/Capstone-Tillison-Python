from rest_framework import serializers
from api.models import Package_Service
from api.Serializers import ServiceSerializer, PackageSerializer

class PackageServiceSerializer(serializers.ModelSerializer):
  service = ServiceSerializer(read_only=True)
  package = PackageSerializer(read_only=True)
  class Meta:
    model = Package_Service
    fields = ["id", "service", "package"]