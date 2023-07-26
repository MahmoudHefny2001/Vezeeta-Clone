from django.urls import path, include
from .views import SignUpView, LoginView, ProfileViewSet, Logout, ChangePasswordView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r"^profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("sign-up/", SignUpView.as_view(), name="user_signup"),
    path("login/", LoginView.as_view(), name="user_signup"),
    path("logout/", Logout.as_view(), name="user_logout"),
    path("password-reset/", ChangePasswordView.as_view(), name="user_change_password"),
]
