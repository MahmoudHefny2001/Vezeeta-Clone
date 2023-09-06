from .views import TimeSlotView
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"", TimeSlotView, basename="time_slot")


urlpatterns = [
    path("", include(router.urls)),
    # path("", ListTimeSlotView.as_view(), name="time_slot_list"),
]