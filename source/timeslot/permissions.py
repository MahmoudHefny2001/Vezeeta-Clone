from rest_framework import permissions
from .models import TimeSlot
 
from doctor.models import DoctorProfile, DoctorExtended


# Allow only the owner of the appointment to view or edit it

class IsAppointmentOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        # get the doctor_profile first from the DoctorExtended model then check 
        # if the doctor_profile is the same as the doctor_profile of the appointment
        # if the doctor_profile is the same, then the doctor is the owner of the appointment
        # return true
        # else, return false

        print("request.user", request.user)
        
        doctor = request.user
        doctor = DoctorExtended.objects.get(id=doctor.id)
        doctor_profile = DoctorProfile.objects.get(doctor=doctor.id)
        if obj.doctor_profile == doctor_profile:
            return True
        return False
    