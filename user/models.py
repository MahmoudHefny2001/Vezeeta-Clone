from django.db import models
from geo.models import Location
from person.models import Person
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class CustomUser(Person):
    base_role = Person.Role.USER

    class Meta:
        proxy = True

    objects = UserManager()


class CustomUserExtended(CustomUser):
    name = models.CharField(max_length=255, blank=True)
    has_medical_insurance = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "account"


class Profile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.OneToOneField(CustomUserExtended, on_delete=models.CASCADE)
    location = models.ForeignKey(
        Location,
        max_length=255,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        default=None,
    )
    points = models.PositiveIntegerField(default=0, null=True, blank=True)
    medical_insurance = models.FileField(
        null=True, blank=True, upload_to="users/insurances"
    )
