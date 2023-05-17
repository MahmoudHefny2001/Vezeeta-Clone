from rest_framework.permissions import BasePermission


class IsAppointmentOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, appointment_obj):
        return appointment_obj.user.id == request.user.id
