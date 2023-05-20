from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

User = get_user_model()


class CustomUserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(email=username) | Q(phone_number=username)
            )
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

