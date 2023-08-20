from django.db import models

from .choices import LOCATION_CHOICES, AREA_OR_CENTER_CHOICES

class City(models.Model):
    class Meta:
        db_table = "city"

    city = models.CharField(choices=LOCATION_CHOICES, null=False, blank=False)    

    def __str__(self) -> str:
        return self.city

class AreaOrCenter(models.Model):
    class Meta:
        db_table = "area_or_center"

    area_or_center = models.CharField(choices=AREA_OR_CENTER_CHOICES, null=False, blank=False)

    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, blank=False)

    location_details = models.TextField()

    def __str__(self) -> str:
        return self.area_or_center