from django.shortcuts import render
from .models import MedicalSpecialty
from .serializers import MedicalSpecialtySerializer
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny


class MedicalSpecialtyView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = MedicalSpecialty.objects.all()
    serializer_class = MedicalSpecialtySerializer
    permission_classes = [AllowAny]
