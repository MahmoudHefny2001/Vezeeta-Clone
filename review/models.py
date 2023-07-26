from django.db import models
from patient.models import Patient, PatientExtended
from django_extensions.db.models import TimeStampedModel
from doctor.models import DoctorProfile
from django.db.models import UniqueConstraint


class Review(TimeStampedModel):
    comment = models.TextField(null=False, blank=False)
    rate = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(PatientExtended, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        db_table = "review"
        unique_together = ["user", "doctor"]

    def __str__(self) -> str:
        return self.comment
