from django.db import models
from geo.models import Location


class Hospital(models.Model):

    class Meta:
        db_table = 'hospital'

    name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=False)
    phone = models.CharField(max_length=20, null=False, blank=False, unique=True, db_index=True)