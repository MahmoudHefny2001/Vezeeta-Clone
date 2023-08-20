from django.db import models
from person.models import Person
from django.utils.translation import gettext_lazy as _
from .managers import PatientManager


class Patient(Person):
    base_role = Person.Role.PATIENT

    class Meta:
        proxy = True

    objects = PatientManager()


class PatientExtended(Patient):
    name = models.CharField(max_length=255, blank=True)
    has_medical_insurance = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "patient"


class PatientProfile(models.Model):
    class Meta:
        db_table = "patient_profile"

    patient = models.OneToOneField(PatientExtended, on_delete=models.CASCADE)
    
    points = models.PositiveIntegerField(default=0, null=True, blank=True)
    