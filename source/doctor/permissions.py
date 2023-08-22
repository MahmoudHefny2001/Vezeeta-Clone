from rest_framework.permissions import BasePermission
from .models import DoctorProfile, DoctorExtended 
from person.models import Person

class IsProfileOwner(BasePermission):  
    pass
    