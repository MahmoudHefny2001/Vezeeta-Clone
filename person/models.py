from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import PersonManager



class Person(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
        DOCTOR = "DOCTOR", "Doctor"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False, unique=True, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    
    objects = PersonManager()

    USERNAME_FIELD = 'email'
    
    class Meta:
        abstract = False
        db_table = 'person'


    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    