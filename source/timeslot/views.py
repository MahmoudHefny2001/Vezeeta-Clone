from django.shortcuts import render
from rest_framework import generics, viewsets, status
from .models import TimeSlot, DateSlot
from .serializers import TimeSlotSerializer, TimeSlotSerializerForDoctors
from rest_framework.permissions import AllowAny, IsAuthenticated
from doctor.models import DoctorProfile, DoctorExtended
from .permissions import IsAppointmentOwner
from rest_framework.response import Response



class TimeSlotView(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializerForDoctors
    permission_classes = [IsAppointmentOwner]


    def get_queryset(self, id=None):

        doctor = self.request.user

        doctor = DoctorExtended.objects.get(id=doctor.id)

        doctor_profile = DoctorProfile.objects.get(doctor_id=doctor.id)


        return TimeSlot.objects.filter(date__doctor_profile=doctor_profile)
    


    def create(self, request, *args, **kwargs):
        date = request.data.get('date', None)
        time = request.data.get('time', None)
        doctor = DoctorExtended.objects.get(id=request.user.id)
        doctor_profile = DoctorProfile.objects.get(doctor=doctor.id)
        date_slot = DateSlot.objects.create(doctor_profile=doctor_profile, date=date)
        time_slot = TimeSlot.objects.create(date=date_slot, start_time=time['start_time'], end_time=time['end_time'])
        serializer = TimeSlotSerializerForDoctors(time_slot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

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
        # get start_time and end_time and is_reserved from request.data
        # update the TimeSlot object with the new data
        # save the TimeSlot object
        # return the updated TimeSlot object

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Partially update the resource with PATCH
        instance = self.get_object()
        if not IsAppointmentOwner().has_object_permission(request, self, instance):
            return Response({"detail": "You do not have permission to update this TimeSlot."}, status=status.HTTP_403_FORBIDDEN)

        time = request.data.get('time', None)
        doctor = DoctorExtended.objects.get(id=request.user.id)
        doctor_profile = DoctorProfile.objects.get(doctor=doctor.id)
        
        
        # Allow null values for is_reserved, start_time, and end_time
        

        is_reserved = time.get('is_reserved', None)
        start_time = time.get('start_time', None)
        end_time = time.get('end_time', None)
        if is_reserved:
            instance.is_reserved = is_reserved
        if start_time:
            instance.start_time = start_time
        if end_time:
            instance.end_time = end_time
        instance.save()
        serializer = TimeSlotSerializerForDoctors(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
