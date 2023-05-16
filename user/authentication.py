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


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            # Perform the token verification
            validated_token = self.get_validated_token(request.data['access_token'])
        except InvalidToken:
            # Handle invalid token exception (e.g., expired or invalid signature)
            return None
        except TokenError:
            # Handle general token error
            return None

        # Check if the token is blacklisted
        if BlacklistedToken.objects.filter(token=str(validated_token)).exists():
            return None  # Token is blacklisted, return None to indicate authentication failure

        # Proceed with regular user retrieval and authentication
        return self.get_user(validated_token), validated_token