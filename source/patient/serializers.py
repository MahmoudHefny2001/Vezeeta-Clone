from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext as _
from .models import Patient, PatientExtended, PatientProfile

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
            # "gender",
            # "birth_date",
            "password",
            # "has_medical_insurance",
        )

    def create(self, validated_data):
        patient = PatientExtended.objects.create_user(**validated_data)
        return patient


    def update(self, instance, validated_data):
        name = validated_data.get("name", None)
        phone_number = validated_data.get("phone_number", None)
        email = validated_data.get("email", None)
        password = validated_data.get("password", None)

        print(validated_data)

        if name:
            instance.name = name
        if phone_number:
            instance.phone_number = phone_number
        if email:
            instance.email = email
        if password:
            instance.set_password(password)
        instance.save()
        return instance



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

    class Meta:
        model = PatientProfile
        fields = ("id", "patient", "points")
        read_only_fields = ("points",)

    
    def create(self, validated_data):
        patient_profile = PatientProfile.objects.create(**validated_data)
        return patient_profile



class OuterViewProfileSerializer(serializers.ModelSerializer):
    patient = OuterViewPatientSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ("id", "patient",)



class PatientSerializerForAppointment(serializers.ModelSerializer):

    class Meta:
        model = PatientExtended
        fields = ('id', 'phone_number', 'gender', 'name', 'has_medical_insurance',)
