from django.db import models
from medical_insurance_firm.models import Firm
from user.models import CustomUser, CustomUserExtended


class MedicalInsurance(models.Model):
    class Meta:
        db_table = "medical_insurance"

    user = models.ForeignKey(CustomUserExtended, on_delete=models.CASCADE)
    medical_insurance_firm = models.ForeignKey(
        Firm, on_delete=models.CASCADE, null=True
    )

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()

    expiray_date = models.DateField()
    medical_insurance_number = models.CharField(
        max_length=100, unique=True, db_index=True
    )
    medical_insurance_image = models.FileField(
        upload_to="users/medical-inusrance", null=True, blank=True
    )
