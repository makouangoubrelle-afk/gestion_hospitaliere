from django.db import models
from django.utils import timezone
from patients.models import Patient
from consultations.models import Consultation


class Invoice(models.Model):
    """Model for medical invoices/bills"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Relationships
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    consultation = models.ForeignKey(Consultation, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Invoice Details
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Tiers payant / Assurance
    assurance_nom = models.CharField(max_length=150, blank=True, null=True)
    assurance_numero = models.CharField(max_length=100, blank=True, null=True)
    montant_assurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_patient = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Description
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.patient.full_name}"
    
    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount
    
    @property
    def is_overdue(self):
        return timezone.now().date() > self.due_date and self.status not in ['paid', 'cancelled']


class InvoiceItem(models.Model):
    """Model for invoice line items"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.description} x {self.quantity}"

