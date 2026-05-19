from django.db import models
from django.contrib.auth.models import AbstractUser

#User roles
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        DOCTOR = 'DOCTOR', 'Doctor'
        NURSE = 'NURSE', 'Nurse'
        PATIENT = 'PATIENT', 'Patient'
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PATIENT
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    def is_clinical_staff(self):
        return self.role in [self.Role.DOCTOR, self.Role.NURSE]

    def __str__(self):
        return f'{self.get_full_name()} ({self.role})'

