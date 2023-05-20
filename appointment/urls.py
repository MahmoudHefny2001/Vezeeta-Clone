from django.urls import path, include
from django.conf import settings
from . import views
from doctor.views import DoctorProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"^doctors", DoctorProfileViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "doctors/<int:doctor_profile_id>/create/",
        views.CreateAppointmentView.as_view(),
        name="create_appointment",
    ),
    path(
        "<int:appointment_id>/",
        views.RetrieveUpdateDeleteAppointmentView.as_view(),
        name="retrieve_update_delete_appointment",
    ),
]
