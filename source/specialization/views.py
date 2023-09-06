from django.shortcuts import render
from . import models, serializers 
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class SpecializationListView(generics.ListAPIView):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.AvaliableSpecializationsSerializer
    permission_classes = [AllowAny,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle,]


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.distinct('specialization')
        return queryset

