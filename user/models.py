from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [('buyer', 'Buyer'), ('seller', 'Seller')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_description = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    def __str__(self):
        return self.username
