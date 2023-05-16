from django.db import models
from django.utils.translation import gettext_lazy as _

class MedicalSpecialty(models.Model):
    description = models.TextField()
    specialty = models.CharField(max_length=100, null=False, blank=False)

    # proof_file = models.FileField(upload_to='doctors/certificates/', null=True, blank=True)