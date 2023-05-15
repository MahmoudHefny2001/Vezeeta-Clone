from django.db import models

class BaseModel(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False, unique=True, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True