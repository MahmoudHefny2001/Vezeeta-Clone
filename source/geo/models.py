from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from .choices import( 
    CITY_CHOICES, 
    AREA_OR_CENTER_CHOICES,
)


class Location(models.Model):
    class Meta:
        db_table = "location"

    city = models.CharField(choices=CITY_CHOICES, null=False, blank=False, db_index=True)
    
    
    def __str__(self):
        # Loop through the CITY_CHOICES to find the corresponding string value
        for value, display_text in CITY_CHOICES:
            if value == self.city:
                return display_text
        return str(self.city)  # Return the numeric value if not found in choices

    

class Address(models.Model):
    class Meta:
        db_table = "address"

    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, default=1)

    name = models.CharField(choices=AREA_OR_CENTER_CHOICES, null=False, blank=False, db_index=True)
    
    location_details = models.TextField()
    

    def __str__(self):
        # Loop through the AREA_OR_CENTER_CHOICES to find the corresponding string value
        for value, display_text in AREA_OR_CENTER_CHOICES:
            if value == self.name:
                return display_text
        return str(self.name)  # Return the numeric value if not found in choices