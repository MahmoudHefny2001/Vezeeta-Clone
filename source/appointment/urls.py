from django.urls import path, include
from django.conf import settings
from . import views
from doctor.views import DoctorProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"yours", views.AppointmentViewSetForDoctors, basename="appointments_doctor")
router.register(r"", views.AppointmentViewSet, basename="appointment")


urlpatterns = [
    path("", include(router.urls)),
    
]
