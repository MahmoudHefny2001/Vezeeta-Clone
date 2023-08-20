from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PatientProfile, PatientExtended, Patient 


@receiver(post_save, sender=PatientExtended)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        PatientProfile.objects.create(patient=instance)
