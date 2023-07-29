from django.db import models
from person.models import Person
from speciality.models import MedicalSpecialty
from clinic.models import Clinic
from geo.models import Location
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from .managers import DoctorManager


class Doctor(Person):
    base_role = Person.Role.DOCTOR

    class Meta:
        proxy = True

    objects = DoctorManager()


class DoctorExtended(Doctor):
    image = models.ImageField(upload_to="doctors/images", null=True, blank=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)

    # Specialization
    specialization = models.ForeignKey(MedicalSpecialty, on_delete=models.PROTECT)

    qualifications = models.TextField(null=False, blank=False)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "doctor"


class DoctorProfile(models.Model):
    class Meta:
        db_table = "doctor_profile"

    doctor = models.OneToOneField(DoctorExtended, on_delete=models.CASCADE)


    # Clinic Information
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)
   
