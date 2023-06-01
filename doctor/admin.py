from django.contrib import admin

from .models import DoctorExtended, DoctorProfile

admin.site.register(DoctorExtended)
admin.site.register(DoctorProfile)
