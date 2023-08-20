from rest_framework import serializers
from patient.serializers import PatientSerializer, OuterViewPatientSerializer
from doctor.serializers import (
    DoctorProfileSerializer,
    # OuterViewDoctorProfileSerializer,
    # AppointmentOuterViewDoctorProfileSerializer,
)
from doctor.models import DoctorProfile
from .models import Appointment
from django.shortcuts import get_object_or_404
from patient.models import PatientExtended


class AppointmentSerializer(serializers.ModelSerializer):
    # doctor_profile = DoctorProfileSerializer(read_only=True)
    # doctor_profile = AppointmentOuterViewDoctorProfileSerializer(read_only=True)

    user = OuterViewPatientSerializer(read_only=True)
    # location = LocationSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ("doctor_profile", "user", "examination_price", "time", "created", "updated")
        read_only_fields = (
            "examination_price",
        )  # Exclude fields from write operations

    def create(self, validated_data):
        doctor_profile_id = self.context["view"].kwargs["doctor_profile_id"]
        doctor_profile = get_object_or_404(DoctorProfile, id=doctor_profile_id)
        user = self.context["request"].user

        # Retrieve the CustomUserExtended instance based on the user object
        custom_user = get_object_or_404(PatientExtended, id=user.id)

        appointment = Appointment.objects.create(
            doctor_profile=doctor_profile,
            user=custom_user,
            examination_price=doctor_profile.examination_price,
        )

        return appointment
