from django.shortcuts import render

from patient.serializers import OuterViewPatientSerializer
from .serializers import AppointmentSerializer, FullAppointmentSerializer, AppointmentSerializerForDoctors
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsAppointmentOwner
from doctor.models import DoctorProfile
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Appointment
from django.shortcuts import get_object_or_404
from patient.models import PatientExtended, PatientProfile
from rest_framework.response import Response
from timeslot.models import TimeSlot
from doctor.models import DoctorExtended


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAppointmentOwner]
    permission_classes = (AllowAny,)



    def get_serializer_class(self):
        if self.action == 'get' or self.action == 'list':
            return FullAppointmentSerializer
        return AppointmentSerializer
            


    def get_queryset(self):
        doctor = self.request.user
        doctor = DoctorExtended.objects.get(id=doctor.id)
        doctor_profile = DoctorProfile.objects.get(doctor=doctor.id)
        
        return Appointment.objects.filter(time_slot__date__doctor_profile=doctor_profile)
    

    # Don't forget to handle permission classes and allow only not reserved appointments to be created and handle number of patients per time slot

    def create(self, request, *args, **kwargs):
        # Get the doctor_profile_id from the request
        doctor_profile_id = self.request.data.get('doctor_profile_id')

        # Get the doctor_profile object
        doctor_profile = DoctorProfile.objects.get(id=doctor_profile_id)
        
        # Get the patient_profile object
        
        patient_phone_number = request.data.get('patient_phone_number', None)
        patient_full_name = request.data.get('patient_full_name', None)
        patient_email = request.data.get('patient_email', None)

        try:
            patient = self.request.user
            patient = PatientExtended.objects.get(id=patient.id)
            # patient_profile = PatientProfile.objects.get(patient=patient.id)
        except:
            patient = PatientExtended.objects.create(
                name=patient_full_name,
                phone_number=patient_phone_number,
                email=patient_email,
            )
        
        # Get the time_slot_id from the request
        time_slot_id = self.request.data.get('time_slot_id')
        # Get the time_slot object
        time_slot = TimeSlot.objects.get(id=time_slot_id)

        # Get the appointment object
        appointment = Appointment.objects.create(
            patient=patient,
            time_slot=time_slot,
        )

        time_slot.is_reserved = True
        time_slot.date.is_reserved = True
        time_slot.save()

        print(time_slot.is_reserved, time_slot.date.is_reserved)

        print(TimeSlot.objects.get(id=time_slot_id).is_reserved, TimeSlot.objects.get(id=time_slot_id).date.is_reserved)

        patient_serializer = OuterViewPatientSerializer(patient)

        # Serialize the appointment object
        serializer = AppointmentSerializer(appointment)
        # Return the serialized appointment object

        

        return Response(
            {
                "appointment": serializer.data, 
                "patient": patient_serializer.data,
            },
            status=status.HTTP_201_CREATED
        )

    

class AppointmentViewSetForDoctors(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializerForDoctors
    permission_classes = [IsAuthenticatedOrReadOnly, IsAppointmentOwner]

    