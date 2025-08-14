from rest_framework.viewsets import ViewSet
from api.models import Review, Package, Package_Service
from rest_framework.response import Response
from rest_framework import status
from api.Serializers import ReviewSerializer
from django.http import HttpResponseServerError
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, permission_classes
from django.contrib.auth import get_user_model

User = get_user_model()

# class ReviewsView(ModelViewSet):
# queryset = Review.objects.select_related("user").all()
# serializer_class = ReviewSerializer


class ReviewsView(ViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
      print("Action:", getattr(self, 'action', None))
      if self.action in ['list', 'retrieve']:
          return [permissions.AllowAny()]
      return [permissions.IsAuthenticated()]

    def list(self, request):
        try:
            reviews = Review.objects.select_related("user").all()
            print("Using ReviewSerializer:", ReviewSerializer)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response(
                {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request, pk=None):
        chosen_package = Package.objects.get(pk=request.data["package_id"])

        review = Review()
        review.description = request.data["description"]
        review.user = request.user
        review.rating = request.data["rating"]
        review.package = chosen_package
        review.save()

        serialized = ReviewSerializer(review, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            review.description = request.data.get("description", review.description)
            review.rating = request.data.get("rating", review.rating)
            review.save()

            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response(
                {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist:
            return Response(
                {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )
