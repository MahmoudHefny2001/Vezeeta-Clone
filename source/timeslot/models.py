import datetime
from django.db import models

from patient.models import PatientProfile, Patient
from doctor.models import DoctorProfile, Doctor


class DateSlot(models.Model):
    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='available_date')

    date = models.DateField(default=datetime.date.today)

    is_reserved = models.BooleanField(default=False, null=True, blank=True)
    
    class Meta:
        db_table = "date_slot"

    def __str__(self) -> str:
        return f"{self.date} is reserved: {self.is_reserved}"

class TimeSlot(models.Model):

    # doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='available_time_slots')

    date = models.ForeignKey(DateSlot, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    is_reserved = models.BooleanField(default=False, null=True, blank=True)


    class Meta:
        db_table = "time_slot"


    # def __str__(self) -> str:
        # return f""
    