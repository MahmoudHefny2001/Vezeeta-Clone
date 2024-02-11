from django.urls import path, include
from django.conf import settings
from . import views
# from doctor.views import DoctorProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"^all", views.ReviwModelViewSet, basename="review")



urlpatterns = [
    path("", include(router.urls)),
    # path(
    # "doctors/<int:doctor_profile_id>/create/",
    # views.CreateReviewView.as_view(),
    # name="create_review",
    # ),
    # path(
        # "doctors/<int:doctor_profile_id>/create/",
        # views.CreateReviewView.as_view(),
        # name="create_review",
    # ),
    # path(
        # "<int:review_id>/",
        # views.RetrieveUpdateDeleteReviewtView.as_view(),
        # name="retrieve_update_delete_review",
    # ),
]
