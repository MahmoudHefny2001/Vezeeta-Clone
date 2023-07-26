from rest_framework import serializers
from .models import Doctor, DoctorProfile, DoctorExtended
from speciality.serializers import MedicalSpecialtySerializer, OuterViewMedicalSpecialtySerializer
from clinic.serializers import ClinicSerializer, OuterViewClinicSerializer
from geo.serializers import LocationSerializer
from speciality.models import MedicalSpecialty
from clinic.models import Clinic
from patient.serializers import ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from geo.models import Location
from review.serializers import ReviewSerializer
from review.models import Review


class DoctorSerializer(serializers.ModelSerializer):
    specialization = MedicalSpecialtySerializer()
    password = serializers.CharField(write_only=True)
    location = LocationSerializer()

    class Meta:
        model = DoctorExtended
        fields = (
            "id",
            "first_name",
            "last_name",
            "image",
            "phone_number",
            "email",
            "specialization",
            "qualifications",
            "password",
            "gender",
            "birth_date",
            "location",
        )

    def create(self, validated_data):
        specialization_data = validated_data.pop("specialization")
        location_data = validated_data.pop("location")
        # Create the nested specialization object
        specialization = MedicalSpecialty.objects.create(**specialization_data)
        location = Location.objects.create(**location_data)
        # Create the Doctor instance
        doctor = DoctorExtended.objects.create_user(
            specialization=specialization, location=location, **validated_data
        )
        return doctor


class OuterViewDoctorSerializer(serializers.ModelSerializer):
    # specialization = MedicalSpecialtySerializer(read_only=True)
    specialization = OuterViewMedicalSpecialtySerializer(read_only=True)
    clinic = OuterViewClinicSerializer(read_only=True)
    class Meta:
        model = DoctorExtended
        fields = ("id", "first_name", "last_name", "image", "clinic", "specialization")


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


class DoctorProfileSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(read_only=True, many=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = "__all__"

    def create(self, validated_data):
        doctor_profile = DoctorProfile.objects.create(**validated_data)
        return doctor_profile

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        reviews = Review.objects.filter(doctor=instance)
        review_serializer = ReviewSerializer(reviews, many=True)
        representation["reviews"] = review_serializer.data
        return representation


class OuterViewDoctorProfileSerializer(serializers.ModelSerializer):
    doctor = OuterViewDoctorSerializer(read_only=True)
    # reviews = ReviewSerializer(read_only=True, many=True)
    clinic = OuterViewClinicSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "doctor",
            "clinic",
            "from_day",
            "to_day",
            "from_hour",
            "to_hour",
            "examination_price",
            # "reviews",
        ]

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     reviews = Review.objects.filter(doctor=instance)
    #     review_serializer = ReviewSerializer(reviews, many=True)
    #     representation["reviews"] = review_serializer.data
    #     return representation


class AppointmentOuterViewDoctorProfileSerializer(serializers.ModelSerializer):
    doctor = OuterViewDoctorSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = "__all__"

    def create(self, validated_data):
        doctor_profile = DoctorProfile.objects.create(**validated_data)
        return doctor_profile

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class ChangePasswordSerializer(serializers.Serializer):
    model = DoctorExtended

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
