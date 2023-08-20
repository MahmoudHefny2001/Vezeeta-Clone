from django.db import models
from patient.models import PatientExtended
from doctor.models import Doctor, DoctorProfile
from django_extensions.db.models import TimeStampedModel 

class Appointment(TimeStampedModel):
    class Meta:
        db_table = "appointment"

    pass
