from rest_framework.permissions import BasePermission
from .models import Review 
from person.models import Person

class IsReviewOwner(BasePermission):  
        
    def has_object_permission(self, request, view, obj):
        return 
    