from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from person.authentication import CustomUserAuthBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer, ProfileSerializer, ChangePasswordSerializer
from rest_framework import status, generics, mixins, viewsets
from django.conf import settings
import jwt
from .models import PatientProfile, PatientExtended
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from django.shortcuts import get_object_or_404
from person.models import Person
from .permissions import IsProfileOwner
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class SignUpView(APIView):
    permission_classes = []

    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


    def post(self, request):
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get("password")
        user = CustomUserAuthBackend().authenticate(
            request=request, username=email_or_phone, password=password
        )

        person = Person.objects.get(email=user.email)
        
        patient = PatientExtended.objects.get(id=person.id)

        profile = PatientProfile.objects.get(patient=patient)

        if user is not None:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                    
                    "username": patient.name,
                    "profile_id": profile.id,
                }
            )
        else:
            return Response(
                {
                    "error": "Invalid credentials",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwner]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


    def get_permissions(self):
        if self.action == "retrieve" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            self.permission_classes = [IsProfileOwner, ]
         
        elif self.action == 'list':
            self.permission_classes = [IsAdminUser, ]
        
        return super(ProfileViewSet, self).get_permissions()


    def get_queryset(self):
        return PatientProfile.objects.filter(patient=self.request.user)
        
    
    

class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the token
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)

            # Blacklist the token
            outstanding_token, _ = OutstandingToken.objects.get_or_create(
                token=str(token)
            )
            BlacklistedToken.objects.create(token=outstanding_token)
            RefreshToken.for_user(request.user)
            # Perform any additional actions or cleanup

            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"Not allowed": "Token is blacklisted"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = PatientExtended
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
