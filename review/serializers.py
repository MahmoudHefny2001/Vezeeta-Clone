from rest_framework import serializers
from .models import Review
from doctor.models import DoctorProfile
from patient.models import PatientExtended
from patient.serializers import PatientReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(serializers.ModelSerializer):
    user = PatientReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "comment",
            "rate",
            "user",
            "created",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        doctor_profile_id = self.context["view"].kwargs["doctor_profile_id"]

        # Check if a review already exists for the user and doctor
        review_exists = Review.objects.filter(
            user=user, doctor=doctor_profile_id
        ).exists()
        if review_exists:
            raise serializers.ValidationError("You have already reviewed this doctor.")

        # Associate the review with the corresponding doctor and user
        doctor_profile = DoctorProfile.objects.get(id=doctor_profile_id)
        review = Review.objects.create(
            user=user, doctor=doctor_profile, **validated_data
        )
        return review
