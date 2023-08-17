from rest_framework import serializers
from .models import Doctor, DoctorProfile, DoctorExtended
from patient.serializers import ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from review.serializers import ReviewSerializer
from review.models import Review


class DoctorSerializer(serializers.ModelSerializer):
    
    specialization = serializers.SerializerMethodField()
    

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
            "location",
            "medical_speciality_description",
            "area_or_center",
            "location_details",
            "specialization",
            "clinic_number",
        )


    def get_specialization(self, obj):
        return dict(obj.SPECIAIALIZATION_CHOICES).get(obj.specialization, '')

    def get_location(self, obj):
        return dict(obj.LOCATION_CHOICES).get(obj.location, '')

    def get_area_or_center(self, obj):
        return dict(obj.AREA_OR_CENTER_CHOICES).get(obj.area_or_center, '')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialization'] = self.get_specialization(instance)
        representation['location'] = self.get_location(instance)
        representation['area_or_center'] = self.get_area_or_center(instance)
        return representation


    def create(self, validated_data):
        doctor = DoctorExtended.objects.create_user(**validated_data)
        return doctor



class OuterViewDoctorSerializer(serializers.ModelSerializer):    

    class Meta:
        model = DoctorExtended
        fields = (
            "id",
            "full_name",
            "image",
            "specialization",
            "qualifications",
            "appointment_price" ,
            "location",
            "medical_speciality_description",
            "area_or_center",
            "location_details",
            "specialization",
            "clinic_number",
        )

    def get_specialization(self, obj):
        return dict(obj.SPECIAIALIZATION_CHOICES).get(obj.specialization, '')

    def get_location(self, obj):
        return dict(obj.LOCATION_CHOICES).get(obj.location, '')

    def get_area_or_center(self, obj):
        return dict(obj.AREA_OR_CENTER_CHOICES).get(obj.area_or_center, '')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialization'] = self.get_specialization(instance)
        representation['location'] = self.get_location(instance)
        representation['area_or_center'] = self.get_area_or_center(instance)
        return representation
    


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
