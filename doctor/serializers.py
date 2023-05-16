from rest_framework import serializers
from .models import Doctor, DoctorProfile
from speciality.serializers import MedicalSpecialtySerializer
from clinic.serializers import ClinicSerializer
from geo.serializers import LocationSerializer
from speciality.models import MedicalSpecialty
from clinic.models import Clinic
from user.serializers import ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError

class DoctorSerializer(serializers.ModelSerializer):
    specialization = MedicalSpecialtySerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name', 'image', 'phone_number', 'email', 'specialization', 'qualifications', 'password', 'gender', 'birth_date')

    def create(self, validated_data):
        specialization_data = validated_data.pop('specialization')
        # Create the nested specialization object
        specialization = MedicalSpecialty.objects.create(**specialization_data)
        # Create the Doctor instance
        doctor = Doctor.objects.create_user(specialization=specialization, **validated_data)
        return doctor


class DoctorProfileSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    class Meta:
        model = DoctorProfile
        fields = '__all__'


    
class ChangePasswordSerializer(serializers.Serializer):
    model = Doctor

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
