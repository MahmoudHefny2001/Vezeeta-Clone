from django.shortcuts import render
from .serializers import AppointmentSerializer, FullAppointmentSerializer
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


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAppointmentOwner]
    permission_classes = [AllowAny]



    def get_serializer_class(self):
        if self.action == 'get' or self.action == 'list':
            return FullAppointmentSerializer
        return AppointmentSerializer
            


    def get_queryset(self):
        patient = self.request.user
        patient = PatientExtended.objects.get(id=patient.id)
        
        return Appointment.objects.filter(patient=patient)
    

    # Don't forget to handle permission classes and allow only not reserved appointments to be created and handle number of patients per time slot

    def create(self, request, *args, **kwargs):
        print("inside create")
        # Get the doctor_profile_id from the request
        doctor_profile_id = self.request.data.get('doctor_profile_id')
        print("doctor_profile_id", doctor_profile_id)

        # Get the doctor_profile object
        doctor_profile = DoctorProfile.objects.get(id=doctor_profile_id)

        print("doctor_profile", doctor_profile)

        # Get the patient_profile object
        patient = self.request.user
        patient = PatientExtended.objects.get(id=patient.id)
        patient_profile = PatientProfile.objects.get(patient=patient.id)
        print("patient_profile", patient_profile)
        
        # Get the time_slot_id from the request
        time_slot_id = self.request.data.get('time_slot_id')
        # Get the time_slot object
        time_slot = TimeSlot.objects.get(id=time_slot_id, doctor_profile=doctor_profile_id)
        # Get the appointment object
        print("time_slot", time_slot)



        appointment = Appointment.objects.create(
            patient=patient,
            time_slot=time_slot,
        )
        # Serialize the appointment object
        serializer = AppointmentSerializer(appointment)
        # Return the serialized appointment object
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    