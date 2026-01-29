"""Views for user registration, authentication and profile management.

Contains endpoints for registering, logging in (JWT), viewing/updating
the authenticated user's profile, changing password and logging out.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import update_session_auth_hash
from .models import User
from .serializers import (UserSerializer, RegisterSerializer, 
                         LoginSerializer, ChangePasswordSerializer,
                         TokenObtainPairEmailSerializer)

class RegisterView(generics.CreateAPIView):
    """Public endpoint to register a new user."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    """Token endpoint for JWT login using email and password."""
    serializer_class = TokenObtainPairEmailSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve/update the currently authenticated user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Validate and apply a password change for the authenticated user."""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            # Verify the old password before making any change.
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Wrong password."}, 
                              status=status.HTTP_400_BAD_REQUEST)

            # Set the new password and persist. `update_session_auth_hash`
            # keeps the user's session valid so they don't get logged out
            # immediately after changing their password.
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({"message": "Password updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Blacklist the provided refresh token to log the user out."""
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token so it can no longer be used to
            # obtain new access tokens. Requires the token_blacklist app.
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
