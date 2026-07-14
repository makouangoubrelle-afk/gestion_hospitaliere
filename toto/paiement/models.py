import uuid

from django.db import models
from django.utils import timezone
from factures.models import Invoice


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Carte bancaire'),
        ('airtel_money', 'Airtel Mobile Money'),
        ('mtn_momo', 'MTN Mobile Money'),
        ('cash', 'Espèces'),
        ('transfer', 'Virement bancaire'),
        ('check', 'Chèque'),
        ('insurance', 'Assurance'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processed', 'Traité'),
        ('completed', 'Confirmé'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Téléphone Mobile Money')
    card_last_four = models.CharField(max_length=4, blank=True, verbose_name='4 derniers chiffres carte')
    notes = models.TextField(blank=True, null=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return f"Paiement {self.transaction_id or self.pk} — {self.amount} ({self.get_status_display()})"

    @staticmethod
    def generate_transaction_id(method):
        prefix = {
            'mtn_momo': 'MTN',
            'airtel_money': 'AIR',
            'card': 'CARD',
        }.get(method, 'PAY')
        return f'{prefix}-{uuid.uuid4().hex[:12].upper()}'

    def complete(self):
        if self.status == 'completed':
            return
        self.status = 'completed'
        self.payment_date = timezone.now()
        self.save(update_fields=['status', 'payment_date', 'updated_at'])
        invoice = self.invoice
        invoice.paid_amount += self.amount
        if invoice.paid_amount >= invoice.total_amount:
            invoice.status = 'paid'
        else:
            invoice.status = 'partial'
        invoice.save(update_fields=['paid_amount', 'status', 'updated_at'])

    def process(self):
        """Compatibilité ascendante."""
        self.complete()


class PaymentMethod(models.Model):
    GATEWAY_CHOICES = [
        ('mtn_momo', 'MTN Mobile Money'),
        ('airtel_money', 'Airtel Mobile Money'),
        ('stripe', 'Carte bancaire (Stripe)'),
        ('wave', 'Wave'),
        ('orangemoney', 'Orange Money'),
        ('local_bank', 'Banque locale'),
    ]

    gateway = models.CharField(max_length=50, choices=GATEWAY_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)
    api_key = models.CharField(max_length=500, blank=True, null=True)
    api_secret = models.CharField(max_length=500, blank=True, null=True)
    webhook_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Passerelle de paiement'
        verbose_name_plural = 'Passerelles de paiement'

    def __str__(self):
        state = 'Active' if self.is_active else 'Inactive'
        return f'{self.get_gateway_display()} — {state}'
