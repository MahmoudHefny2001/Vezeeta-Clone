from rest_framework import serializers
from patient.serializers import PatientSerializer, OuterViewPatientSerializer
from doctor.serializers import (
    DoctorProfileSerializer,
    # OuterViewDoctorProfileSerializer,
    # OuterViewDoctorProfileSerializer,
    AppointmentOuterViewDoctorProfileSerializer,
)
from doctor.models import DoctorProfile
from .models import Appointment
from django.shortcuts import get_object_or_404
from patient.models import PatientExtended
from timeslot.models import TimeSlot
from timeslot.serializers import TimeSlotSerializer, TimeSlotSerializerForPatients


class FullAppointmentSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializerForPatients()
    

    class Meta:
        model = Appointment
        # fields = '__all__'
        exclude = ('modified',)
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = OuterViewPatientSerializer(instance.patient).data
         
        return representation


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        # exclude = ('id', 'doctor_profile', )

    def create(self, validated_data):
        doctor_profile_id = self.validated_data.pop('doctor_profile_id')

        user = self.request.user
        print(user)
        patient = PatientExtended.objects.get(id=user.id)
        print(patient)

        time_slot_id = self.validated_data.pop('time_slot_id')

        timeslot = TimeSlot.objects.get(id=time_slot_id, doctor_profile_id=doctor_profile_id)

        appointment = Appointment.objects.create(
            patient=patient,
            time_slot=timeslot,
            **validated_data
        )
        return appointment