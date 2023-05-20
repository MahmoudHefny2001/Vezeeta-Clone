from django.shortcuts import render
from .models import (
    Doctor, 
    DoctorProfile, 
    DoctorExtended,
)
from .serializers import (
    DoctorSerializer, 
    DoctorProfileSerializer, 
    ChangePasswordSerializer, 
    OuterViewDoctorSerializer,
    OuterViewDoctorProfileSerializer,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import viewsets, generics, mixins, views, permissions
from rest_framework.response import Response
from rest_framework import status
from person.authentication import CustomUserAuthBackend
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from .filters import DoctorFilter



class DoctorSearchAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = DoctorExtended.objects.all()
    serializer_class = OuterViewDoctorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'specialization__speciality', 'qualifications']

class DoctorRegistrationView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        doctor = CustomUserAuthBackend().authenticate(request=request, username=email_or_phone, password=password)
        if doctor is not None:
            access_token = AccessToken.for_user(doctor)
            refresh_token = RefreshToken.for_user(doctor)
            return Response({
                'access': str(access_token),

                'refresh': str(refresh_token),
            })
        else:
            return Response({
                'error': 'Invalid credentials',
            }, status=status.HTTP_401_UNAUTHORIZED)


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = OuterViewDoctorProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Allow any user to list and retrieve doctors
            return [permissions.AllowAny()]
        else:
            # Only authenticated users can perform other actions
            return [permissions.IsAuthenticated()]



class Logout(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get the token
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)

            # Blacklist the token
            outstanding_token, _ = OutstandingToken.objects.get_or_create(token=str(token))
            BlacklistedToken.objects.create(token=outstanding_token)

            # Perform any additional actions or cleanup
            # For example, you can delete any session-related data

            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Token is blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = DoctorExtended
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