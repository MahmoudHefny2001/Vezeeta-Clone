from .views import TimeSlotView, DateSlotView
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"", TimeSlotView, basename="time_slot")
# router.register(r"yourTimes", DateSlotView, basename="date_slot")



urlpatterns = [
    path("", include(router.urls)),
    # path("", ListTimeSlotView.as_view(), name="time_slot_list"),
]