from datetime import timedelta

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from drf_spectacular.utils import extend_schema

from .serializers import LoginResponseSerializer, LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(operation_id="register", request=RegisterSerializer, responses={201: UserSerializer}, auth=[])
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(operation_id="login", request=LoginSerializer, responses={200: LoginResponseSerializer}, auth=[])
    def post(self, request):
        email = request.data.get("email", "").lower()
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        token = AccessToken.for_user(user)
        token["role"] = user.role
        return Response({"access_token": str(token), "token_type": "Bearer", "expires_in": int(timedelta(minutes=60).total_seconds())})
