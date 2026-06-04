from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PropertyCategory(models.Model):
    name = models.CharField(max_length=100, default='Categories')
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

    DOC_STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('NOT_AVAILABLE', 'Not Available'),
    ]

    CONSTRUCTION_STATUS_CHOICES = [
        ('BARE_LAND', 'Bare Land / Unimproved'),
        ('OFF_PLAN', 'Off-Plan'),
        ('UNDER_CONSTRUCTION', 'Under Construction'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    property_address = models.CharField(max_length=200, default='')
    
    # REMOVED max_length=1000 to allow very long, detailed notes
    description = models.TextField(blank=True, help_text="Write a comprehensive, long detailed note about the property features, neighborhood, topography, etc.")
    
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE, related_name='properties')
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='properties')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- DOCUMENTATION STATUS FIELDS ---
    registered_survey = models.CharField(max_length=20, choices=DOC_STATUS_CHOICES, default='NOT_AVAILABLE')
    deed_of_assignment = models.CharField(max_length=20, choices=DOC_STATUS_CHOICES, default='NOT_AVAILABLE')
    building_plan_approval = models.CharField(max_length=20, choices=DOC_STATUS_CHOICES, default='NOT_AVAILABLE')
    c_of_o = models.CharField(verbose_name="C of O", max_length=20, choices=DOC_STATUS_CHOICES, default='NOT_AVAILABLE')
    governors_consent = models.CharField(verbose_name="Governor's Consent", max_length=20, choices=DOC_STATUS_CHOICES, default='NOT_AVAILABLE')

    # --- LAND & BUILDING FEATURE FIELDS ---
    land_size = models.CharField(max_length=100, blank=True, help_text="e.g., '600 sqm' or '2 Plots'")
    sq_meters = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Numeric square meters")
    unit_size = models.CharField(max_length=100, blank=True, null=True, help_text="Built-up area (leave blank for land)")
    construction_status = models.CharField(max_length=30, choices=CONSTRUCTION_STATUS_CHOICES, default='COMPLETED')
    number_of_bedrooms = models.PositiveIntegerField(blank=True, null=True)
    number_of_bathrooms = models.PositiveIntegerField(blank=True, null=True)

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