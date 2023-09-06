from django.shortcuts import render
from rest_framework import generics, viewsets, status
from .models import TimeSlot
from .serializers import TimeSlotSerializer, TimeSlotSerializerForDoctors
from rest_framework.permissions import AllowAny, IsAuthenticated
from doctor.models import DoctorProfile, DoctorExtended
from .permissions import IsAppointmentOwner
from rest_framework.response import Response



class TimeSlotView(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializerForDoctors
    permission_classes = [IsAppointmentOwner]


    def get_queryset(self):
        doctor = self.request.user
        doctor = DoctorExtended.objects.get(id=doctor.id)
        doctor_profile = DoctorProfile.objects.get(doctor=doctor.id)
        return TimeSlot.objects.filter(doctor_profile=doctor_profile)
    


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

    def perform_create(self, serializer):
        doctor = self.request.user
        doctor = DoctorExtended.objects.get(id=doctor.id)
        doctor_profile = DoctorProfile.objects.get(doctor=doctor.id)
        serializer.save(doctor_profile=doctor_profile)

    
    def update(self, request, *args, **kwargs):
        # Get the TimeSlot object to update
        instance = self.get_object()

        # Check if the doctor is the owner of the TimeSlot
        if not IsAppointmentOwner().has_object_permission(request, self, instance):
            return Response({"detail": "You do not have permission to update this TimeSlot."}, status=status.HTTP_403_FORBIDDEN)

        # Serialize the updated data and save it
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    

    def partial_update(self, request, *args, **kwargs):
        # Partially update the resource with PATCH
        instance = self.get_object()
        if not IsAppointmentOwner().has_object_permission(request, self, instance):
            return Response({"detail": "You do not have permission to update this TimeSlot."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)