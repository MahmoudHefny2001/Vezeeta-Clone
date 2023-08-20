from django.db import models
from person.models import Person
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from .managers import DoctorManager

from person.validators import valid_phone_number

from geo.models import Location

from specialization.models import Specialization


class Doctor(Person):
    base_role = Person.Role.DOCTOR

    class Meta:
        proxy = True

    objects = DoctorManager()


class DoctorExtended(Doctor):

    image = models.ImageField(upload_to="doctors/images", null=True, blank=True)
    
    full_name = models.CharField(max_length=100, null=False, blank=False)

    appointment_price = models.PositiveIntegerField(null=False, blank=False)
    
    clinic_number = models.CharField(max_length=20, null=False, blank=False, unique=True, validators=[valid_phone_number])

    qualifications = models.TextField(null=False, blank=False)

    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=False, blank=False)    

    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.full_name}"


    class Meta:
        db_table = "doctor"



class DoctorProfile(models.Model):
    class Meta:
        db_table = "doctor_profile"

    doctor = models.OneToOneField(DoctorExtended, on_delete=models.CASCADE)

   
