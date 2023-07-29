from django.db import models
from speciality.models import MedicalSpecialty
from geo.models import Location


class Clinic(models.Model):
    class Meta:
        db_table = "clinic"

    name = models.CharField(max_length=150, null=False, blank=True)

    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    description = models.TextField()

    clinic_phone = models.CharField(
        max_length=20, null=False, blank=False, unique=True, db_index=True
    )


    # Availability
    from_day = models.CharField(max_length=10, null=True, blank=True)
    to_day = models.CharField(max_length=10, null=True, blank=True)
    from_hour = models.TimeField(null=True, blank=True)
    to_hour = models.TimeField(null=True, blank=True)

    # Pricing
    examination_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )