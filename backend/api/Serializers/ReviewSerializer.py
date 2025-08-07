from rest_framework import serializers
from api.models import Review
from .UserSerializer import UserSerializer
from .PackageSerializer import PackageSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  
    package = PackageSerializer(read_only=True)  
    
    class Meta:
        model = Review
        fields = ['id', 'description', 'rating', 'user', 'package']