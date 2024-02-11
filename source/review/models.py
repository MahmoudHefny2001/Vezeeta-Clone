from django.db import models
from patient.models import Patient, PatientExtended
from django_extensions.db.models import TimeStampedModel
from doctor.models import DoctorProfile, DoctorExtended
from django.db.models import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator
   



class Review(TimeStampedModel):
    comment = models.TextField(null=False, blank=False)
    rate = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(PatientExtended, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        DoctorExtended, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        db_table = "review"
        unique_together = ["user", "doctor"]

    def __str__(self) -> str:
        return f"{self.user: self.comment[0:20] on self.doctor}"
