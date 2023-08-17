from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.utils.translation import gettext_lazy as _



from utils.UniqueRandomNumberGenerator import UniqueRandomNumberGenerator

from django.contrib.auth.hashers import make_password



class PersonManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        try:
            if not email:
                raise ValueError("The Email field must be set")
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(make_password(password))
            user.save()

            return user
        
        except Exception as e:
            raise e

    def create_superuser(self, email, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        generator = UniqueRandomNumberGenerator()
        phone_number = generator.generate_unique_number()  # Adjust the length as needed
        
        return self.create_user(email, password, phone_number=phone_number, **extra_fields)
        
