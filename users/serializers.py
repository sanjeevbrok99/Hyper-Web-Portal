# users/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'password', 'phone', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)  # Hash the password
        user.save()
        return user
class UserLoginSerializer(serializers.Serializer):
    # Define your serializer fields here to handle user login data
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
