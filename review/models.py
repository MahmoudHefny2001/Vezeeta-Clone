from django.db import models
from user.models import CustomUser, CustomUserExtended
from django_extensions.db.models import TimeStampedModel


class BaseReview(TimeStampedModel):
    comment = models.TextField()
    user = models.ForeignKey(CustomUserExtended, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "base_review"


class Review(TimeStampedModel):
    base_review = models.OneToOneField(BaseReview, on_delete=models.CASCADE)

    class Meta:
        db_table = "review"
