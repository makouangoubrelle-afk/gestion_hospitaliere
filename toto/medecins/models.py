from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Medecin(models.Model):
    """Model for hospital doctors"""
    SPECIALTIES = [
        ('general', 'General Practitioner'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('obstetrics', 'Obstetrics & Gynecology'),
        ('surgery', 'Surgery'),
        ('radiology', 'Radiology'),
        ('psychiatry', 'Psychiatry'),
        ('emergency', 'Emergency Medicine'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    
    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES)
    department = models.CharField(max_length=100)
    years_experience = models.IntegerField()
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name_plural = 'Medecins'
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialty})"
    
    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"

