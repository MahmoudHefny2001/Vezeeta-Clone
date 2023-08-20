from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .models import AreaOrCenter, City


@receiver(pre_save, sender=AreaOrCenter)
def validate_city_reference(sender, instance, **kwargs):
    if not instance.city.areaorcenter_set.filter(pk=instance.pk).exists():
        raise ValidationError("Invalid city reference for this area or center.")