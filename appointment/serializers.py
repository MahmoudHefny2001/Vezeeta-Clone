from rest_framework import serializers
from user.serializers import UserSerializer, OuterViewUserSerializer
from doctor.serializers import DoctorProfileSerializer, OuterViewDoctorSerializer
from doctor.models import DoctorProfile
from geo.serializers import LocationSerializer
from .models import Appointment
from django.shortcuts import get_object_or_404

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer(read_only=True)
    user = OuterViewUserSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['location', 'examination_price', 'time']  # Exclude fields from write operations

    def create(self, validated_data):
        doctor_profile_id = self.context['view'].kwargs['doctor_profile_id']
        doctor_profile = get_object_or_404(DoctorProfile, id=doctor_profile_id)
        user = self.context['request'].user

        appointment = Appointment.objects.create(
            doctor_profile=doctor_profile,
            user=user,
            examination_price=doctor_profile.examination_price,
            location=doctor_profile.location,
        )

        return appointment
        