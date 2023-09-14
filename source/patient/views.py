from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from person.authentication import CustomUserAuthBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer, ProfileSerializer
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



    def get_queryset(self):
        patient = PatientExtended.objects.get(id=self.request.user.id)
        return PatientProfile.objects.filter(patient=patient)
        
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()


        patient_data = request.data.get("patient", None)

        

        if patient_data:
            patient_serializer = PatientSerializer(instance.patient, data=patient_data, partial=True)
            patient_serializer.is_valid(raise_exception=True)
            patient_serializer.save()


        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)