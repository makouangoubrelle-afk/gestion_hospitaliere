from django.db import models


class Service(models.Model):
    """Model for hospital services/departments"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Operating Hours
    monday_hours = models.CharField(max_length=50, default="09:00-17:00")
    tuesday_hours = models.CharField(max_length=50, default="09:00-17:00")
    wednesday_hours = models.CharField(max_length=50, default="09:00-17:00")
    thursday_hours = models.CharField(max_length=50, default="09:00-17:00")
    friday_hours = models.CharField(max_length=50, default="09:00-17:00")
    saturday_hours = models.CharField(max_length=50, default="09:00-13:00")
    sunday_hours = models.CharField(max_length=50, default="Closed")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    """Model for service pricing"""
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='prices')
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['service', 'name']
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"

