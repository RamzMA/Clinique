from django.db import models
from django.conf import settings

class Patient(models.Model):
    class BloodType(models.TextChoices):
        A_POS = 'A+'; A_NEG = 'A-'
        B_POS = 'B+'; B_NEG = 'B-'
        AB_POS = 'AB+'; AB_NEG = 'AB-'
        O_POS = 'O+'; O_NEG = 'O-'
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=3, choices=BloodType.choices, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    medical_notes = models.TextField(blank=True, help_text='Visible to clinical staff only')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Patient: {self.user.get_full_name()}'