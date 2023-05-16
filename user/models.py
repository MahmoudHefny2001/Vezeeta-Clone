from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from geo.models import Location
from base.models import BaseModel
from base.models import CustomUserManager
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

class CustomUser(BaseModel):
    name = models.CharField(max_length=255, blank=True)
    has_medical_insurance = models.BooleanField(default=False, null=True, blank=True)
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
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, max_length=255, blank=True, null= True, on_delete=models.SET_NULL, default=None)
    