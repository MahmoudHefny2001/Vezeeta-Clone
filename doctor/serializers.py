from rest_framework import serializers
from .models import Doctor, DoctorProfile
from speciality.serializers import MedicalSpecialtySerializer
from clinic.serializers import ClinicSerializer
from geo.serializers import LocationSerializer


class DoctorSerializer(serializers.ModelSerializer):
    specialization = MedicalSpecialtySerializer()
    clinic = ClinicSerializer(required=False)
    location = LocationSerializer(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'



