from rest_framework.viewsets import ViewSet
from api.Serializers import ServiceSerializer
from api.models import Service
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseServerError


class ServicesView(ViewSet):
  def list(self, request):
    try:
      services = Service.objects.all()
      serializer = ServiceSerializer(services, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as ex:
      return HttpResponseServerError(ex)

  def create(self, request):
    services = Service()
    services.description = request.auth.data["description"]
    services.save()

    serialized = ServiceSerializer(services, many=False)
    return Response(serialized.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk=None):
    try:
      service = Service.objects.get(pk=pk)
      service.description = request.data.get("description", service.description)
      service.save()

      serialized = ServiceSerializer(service)
      return Response(serialized.data, status=status.HTTP_200_OK)

    except Service.DoesNotExist:
      return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
      return HttpResponseServerError(ex)
    

  def retrieve(self, request, pk=None):
    try:
      service = Service.objects.get(pk=pk)
      serializer = ServiceSerializer(service)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Service.DoesNotExist:
      return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

  def destroy(self, request, pk=None):
    try:
      service = Service.objects.get(pk=pk)
      service.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

    except Service.DoesNotExist:
      return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

    



