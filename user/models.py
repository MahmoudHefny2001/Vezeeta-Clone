from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from geo.models import Location

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        print("create_user method called")
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    has_medical_insurance = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, max_length=255, blank=True, null= True, on_delete=models.SET_NULL, default=None)
