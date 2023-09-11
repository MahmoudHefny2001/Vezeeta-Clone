from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import SPECIAIALIZATION_CHOICES


class Specialization(models.Model):
    class Meta:
        db_table = "specialization"

    specialization = models.CharField(choices=SPECIAIALIZATION_CHOICES, null=False, blank=False, db_index=True)

    medical_speciality_description = models.TextField(_("description"), null=True, blank=True)

    def __str__(self):
        # Return the string representation of the specialization model
        self.specialization = dict(SPECIAIALIZATION_CHOICES).get(self.specialization, '')
        return f"{self.specialization}"