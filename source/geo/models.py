from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from .choices import CITY_CHOICES
from . import choices

class Location(models.Model):
    class Meta:
        db_table = "city"

    city = models.CharField(choices=CITY_CHOICES, null=False, blank=False)
    area_or_center = models.CharField(ArrayField(models.CharField(max_length=10, blank=False), size=2))
    
    location_details = models.TextField()

    def __str__(self) -> str:
        return self.city

    def get_valid_areas_for_city(self):
        city_areas = {
            '1': choices.CAIRO_AREAS,
            '2': choices.ALEX_AREAS,
            '3': choices.GIZA_AREAS,
            '4': choices.LUXOR_AREAS,
            '5': choices.ASWAN_AREAS,
            '6': choices.SHARQIA_AREAS,
            '7': choices.GIZA_AREAS,
            '8': choices.PORTSAID_AREAS,
            '9': choices.QALYUBIA_AREAS,
            '10': choices.SOHAG_AREAS,
            '11': choices.MATRUH_AREAS,
            '12': choices.ISMAILIA_AREAS,
            '13': choices.ASYUT_AREAS,
            '14': choices.DAMANHUR_AREAS,
            '15': choices.MINYA_AREAS,
            '16': choices.SUEZ_AREAS,
            '17': choices.DAMIETTA_AREAS,
            '18': choices.BEHEIRA_AREAS,
            '19': choices.FAYOUM_AREAS,
            '20': choices.KAFR_EL_SHEIKH_AREAS,
            '21': choices.QENA_AREAS,
            '22': choices.RED_SEA_AREAS,
            '23': choices.JANZOUR_AREAS,
            '24': choices.SOUTH_SINAI_AREAS,
            # ... (continue with other city areas)
        }
        return city_areas.get(self.city, [])

    def clean(self):
        super().clean()
        self.validate_area_choices()
