from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import status
from api.models import Package_Service, Service, Package
from api.Serializers import PackageServiceSerializer

class PackageServicesView(ViewSet):
  def list(self, request):
    package_service = Package_Service.objects.all()
    serializer = PackageServiceSerializer(package_service, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def retrieve(self, request, pk=None):
    try:
      package_service = Package_Service.objects.get(pk=pk)
      serializer = PackageServiceSerializer(package_service)
      return Response(serializer.data, status=status.HTTP_200_OK)

    except Package_Service.DoesNotExist:
      return Response({"message": "Package_service not found"}, status=status.HTTP_404_NOT_FOUND)

  def create(self, request, pk=None):
    chosen_service = Service.objects.get(pk=request.data['service_id'])
    chosen_package = Package.objects.get(pk=request.data['package_id'])

    package_service = Package_Service()
    package_service.service = chosen_service
    package_service.package = chosen_package
    package_service.save()

    serialized = PackageServiceSerializer(package_service)
    return Response(serialized.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk=None):
    try:
      package_service = Package_Service.objects.get(pk=pk)

      service_id = request.data.get("service_id")
      package_id = request.data.get("package_id")

      if service_id:
        try:
          package_service.service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
          return Response({"message": "Service not found"}, status=status.HTTP_400_BAD_REQUEST)

      if package_id:
        try:
          package_service.package = Package.objects.get(pk=package_id)
        except Package.DoesNotExist:
          return Response({"message": "Package not found"}, status=status.HTTP_400_BAD_REQUEST)

      package_service.save()
      serializer = PackageServiceSerializer(package_service)
      return Response(serializer.data, status=status.HTTP_200_OK)

    except Package_Service.DoesNotExist:
      return Response({"message": "Package_service not found"}, status=status.HTTP_404_NOT_FOUND)

  def destroy(self, request, pk=None):
    try:
      package_service = Package_Service.objects.get(pk=pk)
      package_service.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Package_Service.DoesNotExist:
      return Response({"message": "Package_service not found"}, status=status.HTTP_404_NOT_FOUND)


