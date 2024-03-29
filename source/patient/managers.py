from person.managers import PersonManager
from person.models import Person


class PatientManager(PersonManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Person.Role.PATIENT)
