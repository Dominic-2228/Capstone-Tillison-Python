from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.http import HttpResponseServerError
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(required=False, default=False)
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email", "is_superuser"]
        extra_kwargs = {"password": {"write_only": True}, "is_superuser": {"required": False},}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        is_superuser = request.data.get("is_superuser", False)
        if serializer.is_valid():
            if is_superuser:
                # This sets is_staff=True and is_superuser=True automatically
                user = User.objects.create_superuser(
                    username=serializer.validated_data["username"],
                    password=serializer.validated_data["password"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    email=serializer.validated_data["email"],
                )
            else:
                user = User.objects.create_user(
                    username=serializer.validated_data["username"],
                    password=serializer.validated_data["password"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    email=serializer.validated_data["email"],
                )

            if serializer.validated_data.get("is_superuser", False):
                user.is_superuser = True
                user.is_staff = True   # usually needed so they can access Django admin
                user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def user_login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="profile",
    )
    def profile(self, request):
        """Return data for the currently authenticated user"""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Purpose: Allow a user to communicate with the Bangazon database to retrieve  one user
        Methods:  GET
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to user resource"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)
