import datetime
from django.db import models

from patient.models import PatientProfile, Patient
from doctor.models import DoctorProfile, Doctor


class TimeSlot(models.Model):

    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='available_time_slots')

    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    is_reserved = models.BooleanField(default=False, null=True, blank=True)


    class Meta:
        db_table = "time_slot"


    def __str__(self) -> str:
        return f"{self.doctor_profile.doctor.full_name} available at {self.start_time} on {self.date}"
    