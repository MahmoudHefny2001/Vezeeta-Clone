from django.db import models
from patient.models import PatientExtended
from doctor.models import Doctor, DoctorProfile
from django_extensions.db.models import TimeStampedModel 

class Appointment(TimeStampedModel):
    class Meta:
        db_table = "appointment"

    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(PatientExtended, on_delete=models.CASCADE)

    # def get_default_location(self):
    #     return self.doctor_profile.location

    # def get_default_price(self):
    #     return self.doctor_profile.examination_price

    # location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    examination_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=False,
        # default=get_default_price,
    )
    time = models.DateTimeField(auto_now_add=True)
