from django.db import models
from django.utils.translation import gettext_lazy as _

class MedicalSpecialty(models.Model):
    SPECIALTY_CHOICES = [
        ('allergy_immunology', _('Allergy and Immunology')),
        ('anesthesiology', _('Anesthesiology')),
        ('dermatology', _('Dermatology')),
        ('emergency_medicine', _('Emergency Medicine')),
        ('family_medicine', _('Family Medicine')),
        ('gastroenterology', _('Gastroenterology')),
        ('general_surgery', _('General Surgery')),
        ('internal_medicine', _('Internal Medicine')),
        ('neurology', _('Neurology')),
        ('obstetrics_gynecology', _('Obstetrics and Gynecology')),
        ('ophthalmology', _('Ophthalmology')),
        ('orthopedic_surgery', _('Orthopedic Surgery')),
        ('otolaryngology', _('Otolaryngology')),
        ('pediatrics', _('Pediatrics')),
        ('psychiatry', _('Psychiatry')),
        ('radiology', _('Radiology')),
        ('urology', _('Urology')),
        # Add more specialties here...
    ]

    description = models.TextField()
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, verbose_name=_('Specialty'))