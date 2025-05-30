from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Chef', 'Oshpaz'),
        ('Manager', 'Menejer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Chef')
    def __str__(self):
        return self.username