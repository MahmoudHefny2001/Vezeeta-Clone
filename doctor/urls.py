from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", views.DoctorProfileViewSet)

router.register(r"^profiles-for-doctors", views.DoctorProfileViewSet_Doctors)


urlpatterns = [
    path("sign-up/", views.DoctorRegistrationView.as_view(), name="doctor-registration"),
    path("login/", views.LoginView.as_view(), name="doctor-login"),
    path("logout/", views.Logout.as_view(), name="doctor-logout"),
    path("change-password/", views.ChangePasswordView.as_view()),
    
    path("", include(router.urls)),
]
