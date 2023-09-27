from django.urls import path, include
from .views import SignUpView, LoginView, ProfileViewSet, PatientViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r"^profiles", ProfileViewSet, basename="patient-profiles")


urlpatterns = [
    path('', include(router.urls)),
    path("sign-up/", SignUpView.as_view(), name="patients-signup"),
    path("login/", LoginView.as_view(), name="patients-login"),

]
