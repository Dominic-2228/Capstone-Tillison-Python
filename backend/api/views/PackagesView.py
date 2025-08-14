from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import status
from api.models import Package
from api.Serializers import PackageSerializer
from rest_framework import viewsets, status, permissions

class PackageView(ViewSet):
  def get_permissions(self):
        # Allow anyone to list or retrieve packages
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]  # for create/update/delete
        return [p() for p in permission_classes]
  
  def list(self, request):
    try:
      package = Package.objects.all()
      serializer = PackageSerializer(package, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as ex:
      return HttpResponseServerError(ex)
    
  def retrieve(self, request, pk=None):
        try:
            package = Package.objects.get(pk=pk)
            serializer = PackageSerializer(package)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            return Response({"message": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

  def update(self, request, pk=None):
        try:
            package = Package.objects.get(pk=pk)
            serializer = PackageSerializer(package, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Package.DoesNotExist:
            return Response({"message": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

  def destroy(self, request, pk=None):
        try:
            package = Package.objects.get(pk=pk)
            package.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Package.DoesNotExist:
            return Response({"message": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

  def create(self, request):
    serializer = PackageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)