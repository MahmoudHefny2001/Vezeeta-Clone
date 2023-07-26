from django.contrib import admin
from .models import PatientExtended, PatientProfile

# Register your models here.


admin.site.register(PatientExtended)
admin.site.register(PatientProfile)