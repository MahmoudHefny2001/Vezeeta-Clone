from rest_framework import serializers
from .models import Doctor, DoctorProfile, DoctorExtended
from speciality.serializers import MedicalSpecialtySerializer
from clinic.serializers import ClinicSerializer
from geo.serializers import LocationSerializer
from speciality.models import MedicalSpecialty
from clinic.models import Clinic
from user.serializers import ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from geo.models import Location


class DoctorSerializer(serializers.ModelSerializer):
    specialization = MedicalSpecialtySerializer()
    password = serializers.CharField(write_only=True)
    location = LocationSerializer()
    
    class Meta:
        model = DoctorExtended
        fields = (
            'id', 
            'first_name', 'last_name', 'image', 
            'phone_number', 'email', 'specialization', 
            'qualifications', 'password', 'gender', 
            'birth_date', 'location')


    def create(self, validated_data):
        specialization_data = validated_data.pop('specialization')
        location_data = validated_data.pop('location')
        # Create the nested specialization object
        specialization = MedicalSpecialty.objects.create(**specialization_data)
        location = Location.objects.create(**location_data)
        # Create the Doctor instance
        doctor = DoctorExtended.objects.create_user(specialization=specialization, location=location, **validated_data)
        return doctor



class OuterViewDoctorSerializer(serializers.ModelSerializer):
    specialization = MedicalSpecialtySerializer(read_only=True)
    class Meta:
        model = DoctorExtended
        fields = ('id', 'first_name', 'last_name', 'image', 'specialization')


class DoctorProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DoctorProfile
        fields = '__all__'
    
    doctor = DoctorSerializer(read_only=True)

    def create(self, validated_data):
        doctor_profile = DoctorProfile.objects.create(**validated_data)
        return doctor_profile
    

class OuterViewDoctorProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'doctor', 'clinic', 
            'from_day', 'to_day', 'from_hour',
            'to_hour', 'examination_price'
        ]
    
    doctor = OuterViewDoctorSerializer(read_only=True)


    
class ChangePasswordSerializer(serializers.Serializer):
    model = DoctorExtended

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
