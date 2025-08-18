from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import status, permissions
from api.models import Booking_time
from api.Serializers import BookingTimeSerializer

class BookingTimesView(ViewSet):
    def get_permissions(self):
        # Allow anyone to list or retrieve packages
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]  # for create/update/delete
        return [p() for p in permission_classes]

    def list(self, request):
        booking_time = Booking_time.objects.all()
        serializer = BookingTimeSerializer(booking_time)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
    def retrieve(self, request, pk=None):
        try:
            booking_time = Booking_time.objects.get(pk=pk)
            serializer = BookingTimeSerializer(booking_time)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking_time.DoesNotExist:
            return Response({"message": "Booking time not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = BookingTimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Validation Errors:", serializer.errors)  # <-- Add this
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            booking_time = Booking_time.objects.get(pk=pk)
            serializer = BookingTimeSerializer(booking_time, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Booking_time.DoesNotExist:
            return Response({"message": "Booking time not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            booking_time = Booking_time.objects.get(pk=pk)
            booking_time.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Booking_time.DoesNotExist:
            return Response({"message": "Booking time not found"}, status=status.HTTP_404_NOT_FOUND)
