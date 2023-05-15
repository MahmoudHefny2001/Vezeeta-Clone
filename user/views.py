from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .authentication import CustomUserAuthBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileSerializer, ChangePasswordSerializer
from rest_framework import status, generics, mixins, viewsets
from django.conf import settings
import jwt
from .models import CustomUser, Profile
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken



class SignUpView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        user = CustomUserAuthBackend().authenticate(request=request, username=email_or_phone, password=password)

        if user is not None:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'access': str(access_token),

                'refresh': str(refresh_token),
            })
        else:
            return Response({
                'error': 'Invalid credentials',
            }, status=status.HTTP_401_UNAUTHORIZED)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=user)
    

class Logout(APIView):
    def post(self, request):
        # Revoke the user's tokens
        token = request.data.get('token')
        if token:
            BlacklistedToken.objects.create(token=token)
        # Perform any additional actions or return a response as needed
        return Response({"detail": "Logout successful"})


class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = CustomUser
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    