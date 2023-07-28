# users/views.py
import token
from django.db.models import Q
from rest_framework import generics
from .models import User
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.hashers import check_password

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        email = self.request.query_params.get('email', None)

        if name and email:
            queryset = queryset.filter(Q(name__icontains=name) | Q(email=email))
        elif name:
            queryset = queryset.filter(name__icontains=name)
        elif email:
            queryset = queryset.filter(email=email)

        return queryset

class UserRetrieveByEmailView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        email = self.request.query_params.get('email', None)

        if email:
            queryset = queryset.filter(email=email)

        return queryset
    


class UserLogin(APIView):
    """
    Log in a user and generate JWT tokens
    """
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Perform any additional validation or logic specific to user login if needed
            # For example, you can check if the user exists, if the provided password is correct, etc.

            # If the provided credentials are valid, you can generate JWT tokens
            validated_data = serializer.validated_data  # Get the validated user data from the serializer

            # Assuming the serializer has validated 'username' and 'password'
            username = validated_data['username']
            password = validated_data['password']

            try:
                # Retrieve the user object based on the provided username
                user = User.objects.get(username=username)
                print(user)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # Perform authentication logic here by checking the provided password
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # If the password is valid, generate an access token and refresh token for the user
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)

            # Optionally, you can add more data to the token's payload (e.g., user roles, permissions)
            # access_token['role'] = user.role

            # Create a dictionary containing the access and refresh tokens
            tokens = {
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }

            # Optionally, you can perform additional actions here (e.g., log login activity)

            return Response(tokens, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)