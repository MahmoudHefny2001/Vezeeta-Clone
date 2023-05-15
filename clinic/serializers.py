from rest_framework import serializers
from .models import Clinic
from speciality.models import MedicalSpecialty

class ClinicSerializer(serializers.ModelSerializer):
    specialties = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=MedicalSpecialty.objects.all()
    )
    class Meta:
        model = Clinic
        fields = '__all__'
