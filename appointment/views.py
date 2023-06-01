from django.shortcuts import render
from .serializers import AppointmentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsAppointmentOwner
from doctor.models import DoctorProfile
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Appointment
from django.shortcuts import get_object_or_404
from user.models import CustomUserExtended, Profile


class CreateAppointmentView(CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        custom_user = get_object_or_404(CustomUserExtended, id=user.id)

        user_profile = get_object_or_404(Profile, user_id=user.id)
        user_profile.points += 100
        user_profile.save()

        doctor_profile_id = self.kwargs["doctor_profile_id"]
        doctor_profile = get_object_or_404(DoctorProfile, id=doctor_profile_id)
        serializer.save(user=custom_user, doctor_profile=doctor_profile)


class RetrieveUpdateDeleteAppointmentView(RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_url_kwarg = "appointment_id"
    lookup_field = "id"
    permission_classes = [IsAppointmentOwner]
