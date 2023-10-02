from django.shortcuts import render
from rest_framework import generics, viewsets, status
from .models import TimeSlot, DateSlot
from .serializers import TimeSlotSerializer, TimeSlotSerializerForDoctors
from rest_framework.permissions import AllowAny, IsAuthenticated
from doctor.models import DoctorProfile, DoctorExtended
from .permissions import IsAppointmentOwner
from rest_framework.response import Response

from django.utils import timezone


from .serializers import DateSlotSerializer

class TimeSlotView(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializerForDoctors
    permission_classes = [IsAppointmentOwner]


    def get_queryset(self, id=None):
        queryset = self.queryset
        doctor = self.request.user

        doctor = DoctorExtended.objects.get(id=doctor.id)

        doctor_profile = DoctorProfile.objects.get(doctor_id=doctor.id)

        queryset = queryset.filter(date__doctor_profile=doctor_profile.id)
        # queryset = queryset.filter(date__date__gte=timezone.now()).order_by('date__date', 'start_time')

        return queryset
    


    def create(self, request, *args, **kwargs):
        
        user = request.user
        doctor = DoctorExtended.objects.get(id=user.id)
        doctor_profile = DoctorProfile.objects.get(doctor=doctor.id)
            
        date = request.data['date']
        time = request.data['time']
        
        date_slot = None
        
        start_time = time['start_time']
        end_time = time['end_time']
        is_reserved = time.get('is_reserved', None)
        check_date = DateSlot.objects.filter(date=date, doctor_profile=doctor_profile).first()
        if not check_date:
            date_slot = DateSlot.objects.create(date=date, doctor_profile=doctor_profile)
            date_slot.save()
            time_slot = TimeSlot.objects.create(date=date_slot, start_time=start_time, end_time=end_time, is_reserved=is_reserved)
            time_slot.save()
            
        else:
            time_slot = TimeSlot.objects.create(date=check_date, start_time=start_time, end_time=end_time, is_reserved=is_reserved)
            time_slot.save()
        
        return Response(
            {
                "status": "success",
                "message": "TimeSlot created successfully",
                "data": {
                    "date": time_slot.date.date,
                    "time": TimeSlotSerializer(time_slot).data},
            },
            status=status.HTTP_201_CREATED,
        )
    
    
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
        # Get the TimeSlot object to update
        instance = self.get_object()
        print("Instance", instance)
        # Check if the doctor is the owner of the TimeSlot
        if not IsAppointmentOwner().has_object_permission(request, self, instance):
            return Response({"detail": "You do not have permission to update this TimeSlot."}, status=status.HTTP_403_FORBIDDEN)
        
        # Serialize the updated data and save it
        # get start_time and end_time and is_reserved from request.data
        # update the TimeSlot object with the new data
        # save the TimeSlot object
        # return the updated TimeSlot object

        print("Date", request.data)

        time = request.data['time']
        start_time = time.get('start_time', None)
        end_time = time.get('end_time', None)
        is_reserved = time.get('is_reserved', None)
        
        if start_time:
            instance.start_time = start_time
        if end_time:
            instance.end_time = end_time
        if is_reserved:
            instance.is_reserved = is_reserved
        instance.save()
        return Response(TimeSlotSerializer(instance).data)
        
    


class DateSlotView(viewsets.ModelViewSet):
    queryset = DateSlot.objects.all()
    serializer_class = DateSlotSerializer
    permission_classes = [IsAppointmentOwner,]
    
    def get_queryset(self, id=None):
        queryset = self.queryset
        
        doctor = DoctorExtended.objects.get(id=self.request.user.id)

        doctor_profile = DoctorProfile.objects.get(doctor_id=doctor.id)

        queryset = queryset.filter(doctor_profile=doctor_profile.id)
        
        return queryset
    


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    


    # def update(self, request, *args, **kwargs):
        