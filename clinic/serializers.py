from rest_framework import serializers
from .models import Clinic
from speciality.models import MedicalSpecialty
from geo.serializers import LocationSerializer


class ClinicSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Clinic
        fields = '__all__'


class OuterViewClinicSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Clinic
        fields = ('name', 'location', 'clinic_phone', 'examination_price',)