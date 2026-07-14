from django.db import models
from django.utils import timezone
from patients.models import Patient
from medecins.models import Medecin


class Consultation(models.Model):
    """Model for medical consultations"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    VISIT_TYPE_CHOICES = [
        ('outpatient', 'Outpatient'),
        ('inpatient', 'Inpatient'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
    ]
    
    # Relationships
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medecin = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, related_name='consultations')
    
    # Consultation Details
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES)
    appointment_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=30)
    
    # Medical Information
    chief_complaint = models.TextField()
    diagnosis = models.TextField(blank=True, null=True)
    cim10_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Code CIM-10')
    treatment_plan = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    version = models.PositiveIntegerField(default=1)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date']
    
    def __str__(self):
        return f"Consultation - {self.patient.full_name} with Dr. {self.medecin.last_name} ({self.appointment_date})"

