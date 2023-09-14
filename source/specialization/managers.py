from django.db import models

from .choices import SPECIAIALIZATION_CHOICES


class SpecializationManager(models.Manager):
    def get_or_create_by_code_or_name(self, code_or_name, medical_speciality_description=None):
                
        # Check if the code_or_name is a numeric string
        if code_or_name.isdigit():
            # If it's a numeric string, assume it's a code and try to find the specialization by code
            specialization, created = self.get_or_create(speciality=code_or_name).first()
        else:
            # If it's not a numeric string, assume it's a name and try to find the specialization by name

            if code_or_name in dict(SPECIAIALIZATION_CHOICES).values():
                
                for key, value in dict(SPECIAIALIZATION_CHOICES).items():
                    if value == code_or_name:
                        code_or_name = key
                        break

                specialization, created = self.get_or_create(
                    speciality= code_or_name
                ).first()
            else:
                return None, False
        return specialization, created        

        