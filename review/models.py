from django.db import models
from user.models import CustomUser
from django_extensions.db.models import TimeStampedModel

class BaseReview(TimeStampedModel):
    review = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()