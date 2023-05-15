from django.shortcuts import render
from .models import Clinic
from .serializers import ClinicSerializer
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny


class ClinicViewSet(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [AllowAny]