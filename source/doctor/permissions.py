from rest_framework.permissions import BasePermission
from .models import DoctorProfile, DoctorExtended 
from person.models import Person

from rest_framework.permissions import SAFE_METHODS

class IsObjectOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to any user (including anonymous)
    while restricting other methods (PUT, PATCH, DELETE, etc.) to the object's owner.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated


    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
 
        if request.method in SAFE_METHODS:
            return True

        # print("User: ", request.user.email, "Object: " , obj)
        return obj.doctor.email == request.user.email