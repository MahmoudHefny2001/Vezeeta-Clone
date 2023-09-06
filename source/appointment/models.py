from django.db import models
from patient.models import PatientExtended
from doctor.models import Doctor, DoctorProfile
from django_extensions.db.models import TimeStampedModel 
from timeslot.models import TimeSlot


class Appointment(TimeStampedModel):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='time_slots_appointments')
    patient = models.ForeignKey(PatientExtended, on_delete=models.CASCADE, related_name='patient_appointments')
    