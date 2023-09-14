from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", views.DoctorProfileViewSet, basename="doctor")

router.register(r"^profiles", views.DoctorProfileViewSetForDoctors, basename="profiles")

urlpatterns = [    

    path("sign-up/", views.DoctorRegistrationView.as_view(), name="doctor-registration"),
    path("login/", views.LoginView.as_view(), name="doctor-login"),
    
    path("", include(router.urls)),
]
