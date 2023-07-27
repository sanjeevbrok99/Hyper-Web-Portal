# users/views.py
from django.db.models import Q
from rest_framework import generics
from .models import User
from .serializers import UserSerializer

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