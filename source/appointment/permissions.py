from rest_framework.permissions import BasePermission


class IsAppointmentOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, appointment_obj):
        return True
