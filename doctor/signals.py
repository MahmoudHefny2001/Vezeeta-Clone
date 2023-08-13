from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor, DoctorProfile, DoctorExtended


@receiver(post_save, sender=DoctorExtended)
def create_doctor_profile(sender, instance, created, **kwargs):
    try:
        if created and instance.role == "DOCTOR":
            doctorprofile = doctorprofile.objects.create(doctor=instance)
            doctorprofile.save()
    except Exception as e:
        print(e)
