from django.db import models
from speciality.models import MedicalSpecialty
from geo.models import Location


class Clinic(models.Model):
    name = models.CharField(max_length=150, null=False, blank=True)

    specialties = models.ManyToManyField(MedicalSpecialty)

    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    description = models.TextField()

    clinic_phone = models.CharField(max_length=20, null=False, blank=False, unique=True, db_index=True)
    