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

from geo.models import Location, Address

from specialization.models import Specialization

# from timeslot.models import TimeSlot


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

    address = models.ForeignKey(Address, on_delete=models.SET_DEFAULT, null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.id} - {self.full_name}"
    
    



    class Meta:
        db_table = "doctor"



class DoctorProfile(models.Model):
    class Meta:
        db_table = "doctor_profile"

    doctor = models.OneToOneField(DoctorExtended, on_delete=models.CASCADE)

    
    
    # waiting_duration = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"profile {self.id} of {self.doctor.full_name}"