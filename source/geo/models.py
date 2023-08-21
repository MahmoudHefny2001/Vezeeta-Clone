from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from .choices import( 
    CITY_CHOICES, 
    AREA_OR_CENTER_CHOICES,
    #ALL_AREAS,
)


class Location(models.Model):
    class Meta:
        db_table = "city"

    city = models.CharField(choices=CITY_CHOICES, null=False, blank=False, db_index=True)
    

    def __str__(self) -> str:
        return self.city

    

class Address(models.Model):
    class Meta:
        db_table = "address"

    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    # name = models.CharField(choices=ALL_AREAS, null=False, blank=False)
    name = models.CharField(choices=AREA_OR_CENTER_CHOICES, null=False, blank=False, db_index=True)

    location_details = models.TextField()

    def __str__(self) -> str:
        return f"self.name"