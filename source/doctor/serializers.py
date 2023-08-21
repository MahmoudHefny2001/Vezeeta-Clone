from rest_framework import serializers
from .models import Doctor, DoctorProfile, DoctorExtended
from patient.serializers import ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from review.serializers import ReviewSerializer
from review.models import Review

from geo.serializers import LocationSerializer, AddressSerializer
from specialization.serializers import SpecializationSerializer


class DoctorSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DoctorExtended
        fields = (
            "id",           
            "full_name",
            "image",
            "phone_number",
            "email",
            "qualifications",
            "password",
            "gender",
            "birth_date",
            "appointment_price" ,
            "specialization",
            "clinic_number",
            "address",
        )

    
    def create(self, validated_data):
        specialization = validated_data.pop("specialization")
        address = validated_data.pop("address")

        doctor = DoctorExtended.objects.create_user(
            specialization=specialization,
            address=address,
            **validated_data
        )
        return doctor



class OuterViewDoctorSerializer(serializers.ModelSerializer):    

    specialization = SpecializationSerializer()

    # area_or_center = AreaOrCenterSerializer()
    address = AddressSerializer()

    class Meta:
        model = DoctorExtended
        fields = (
            "id",
            "full_name",
            "image",
            "qualifications",
            "appointment_price" ,
            "address",
            "specialization",
            "clinic_number",
        )
    

class OuterViewDoctorProfileSerializer(serializers.ModelSerializer):
    doctor = OuterViewDoctorSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ("id", "doctor",)


class DoctorProfileSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(read_only=True, many=True)
    doctor = OuterViewDoctorSerializer(read_only=True)
    
    class Meta:
        model = DoctorProfile
        fields = '__all__'



class DoctorProfileSerializerForDoctors(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = "__all__"

    def create(self, validated_data):
        doctor_profile = DoctorProfile.objects.create(**validated_data)
        return doctor_profile

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
