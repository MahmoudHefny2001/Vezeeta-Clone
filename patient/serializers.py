from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext as _
from .models import Patient, PatientExtended, PatientProfile
from geo.models import Location
from geo.serializers import LocationSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework.response import Response
from rest_framework import status


User = get_user_model()


class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = PatientExtended
        fields = (
            "id",
            "name",
            "phone_number",
            "email",
            "gender",
            "birth_date",
            "password",
            "has_medical_insurance",
        )

    def create(self, validated_data):
        patient = PatientExtended.objects.create_user(**validated_data)
        return patient



class OuterViewPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientExtended
        fields = ("id", "name", "phone_number", "email", "has_medical_insurance")



class PatientReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientExtended
        fields = ("id", "name")


class ProfileSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    location = LocationSerializer(required=False)

    class Meta:
        model = PatientProfile
        fields = ("id", "patient", "location", "points")
        read_only_fields = ("points",)

    def create(self, validated_data):
        location_data = validated_data.pop("location")
        location = Location.objects.create(**location_data)
        profile = PatientProfile.objects.create(location=location, **validated_data)
        return profile

    def update(self, instance, validated_data):
        location_data = validated_data.pop("location")
        location_serializer = LocationSerializer(
            instance.location, data=location_data, partial=True
        )
        if location_serializer.is_valid():
            location = location_serializer.save()
        else:
            raise serializers.ValidationError(location_serializer.errors)
        instance.location = location

        instance.save()
        return instance



class OuterViewProfileSerializer(serializers.ModelSerializer):
    patient = OuterViewPatientSerializer(read_only=True)
    location = LocationSerializer(required=False)

    class Meta:
        model = PatientProfile
        fields = ("id", "patient", "location")



class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
