from django.urls import path
from .views import MedicalSpecialtyView

urlpatterns = [
    path("", MedicalSpecialtyView.as_view(), name="medical-specialties"),
]
