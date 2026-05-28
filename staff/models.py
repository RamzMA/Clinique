from django.db import models
from django.conf import settings

#Department model for deperament name
class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    specialisation = models.CharField(max_length=100, blank=True)
    licence_number = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.role}: {self.user.get_full_name()}'
    
