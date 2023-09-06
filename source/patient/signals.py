from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PatientProfile, PatientExtended, Patient 


@receiver(post_save, sender=PatientExtended)
def create_patient_profile(sender, instance, created, **kwargs):
    try:
        if created and instance.role == "PATIENT":
            patient_profile = PatientProfile.objects.create(patient=instance)
            patient_profile.save()
    except Exception as e:
        print(e)
        
    