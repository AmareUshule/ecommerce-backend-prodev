"""Serializers for user registration, authentication and profiles.

Includes registration/login serializers and a JWT token serializer
extension that returns serialized user data alongside tokens.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the `UserProfile` model."""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'date_of_birth', 'gender']

class UserSerializer(serializers.ModelSerializer):
    """Full user serializer including nested `UserProfile`."""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 
                 'address', 'is_email_verified', 'profile', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_email_verified']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password confirmation."""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    """Simple credential serializer used for non-JWT login flows."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled")
        return {'user': user}


class TokenObtainPairEmailSerializer(TokenObtainPairSerializer):
    """Extend TokenObtainPairSerializer to include serialized user data in response.

    This serializer relies on the project's `AUTH_USER_MODEL` having
    `USERNAME_FIELD = 'email'`, so it accepts `email` and `password` in the
    request body (the base class respects the user model username field).
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        # include user details
        user_data = UserSerializer(self.user).data
        data.update({'user': user_data})
        return data

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing an authenticated user's password."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
