from rest_framework.permissions import BasePermission
from .models import DoctorProfile, DoctorExtended 
from person.models import Person

class IsProfileOwner(BasePermission):  
        
    def has_object_permission(self, request, view, obj):
        return obj.doctor.email == request.user.email or obj.doctor.phone_number == request.user.phone_number