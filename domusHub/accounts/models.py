from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = [
        ("ESTATE AGENT", 'Estate Agent'),
        ("INDIVIDUAL", 'Individual'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES )
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

class AgentProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='agent_meta')
    license_number = models.CharField(max_length=50)
    agency_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Agent {self.profile.user.username}'
