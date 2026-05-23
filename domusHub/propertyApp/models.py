from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PropertyCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    

class Property(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('PENDING', 'Pending'),
        ('UNDER_OFFER', 'Under Offer'),
        ('SOLD', 'Sold'),
    ]

    title = models.CharField(max_length=200)
    property_address = models.CharField(max_length=200, default='Nigeria')
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE, related_name='properties')
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='properties')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})' 

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f'{self.user.username} - {self.property.title}'