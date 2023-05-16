from django.db import models
from base.models import BaseModel
from speciality.models import MedicalSpecialty
from clinic.models import Clinic
from geo.models import Location
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from base.models import CustomUserManager
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class Doctor(BaseModel):

    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    
    # Specialization
    specialization = models.ForeignKey(MedicalSpecialty, on_delete=models.PROTECT)
    qualifications = models.TextField(null=False, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="doctor_user_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="doctor_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']


    class Meta:
        default_related_name = 'doctor_users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DoctorProfile(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    
    # Clinic Information
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)

    # Availability
    from_day = models.CharField(max_length=10, null=True, blank=False)
    to_day = models.CharField(max_length=10, null=True, blank=False)
    from_hour = models.TimeField(null=True, blank=False)
    to_hour = models.TimeField(null=True, blank=False)

    # Pricing
    examination_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)

    # Location
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=False)


