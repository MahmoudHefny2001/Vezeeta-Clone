from rest_framework.permissions import BasePermission
from .models import PatientProfile, PatientExtended 
from person.models import Person

class IsProfileOwner(BasePermission):  
        
    def has_object_permission(self, request, view, obj):
        pass