from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile, CustomUserExtended


@receiver(post_save, sender=CustomUserExtended)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
