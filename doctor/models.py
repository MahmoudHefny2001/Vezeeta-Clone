from django.db import models
from base.models import BaseModel
from speciality.models import MedicalSpecialty
from clinic.models import Clinic
from geo.models import Location
class Doctor(BaseModel):

    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    
    # Specialization
    specialization = models.ForeignKey(MedicalSpecialty, on_delete=models.PROTECT)
    qualifications = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name



class DoctorProfile(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)

    # Clinic Information
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)

    # Availability
    from_day = models.CharField(max_length=10)
    to_day = models.CharField(max_length=10)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    # Pricing
    examination_price = models.DecimalField(max_digits=5, decimal_places=2)

    # Location
    location = models.ForeignKey(Location, on_delete=models.PROTECT)