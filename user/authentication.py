from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import BaseBackend


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