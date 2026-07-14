import re
from decimal import Decimal

from django.core.exceptions import ValidationError

from .models import Payment

MOBILE_METHODS = {'mtn_momo', 'airtel_money'}
PHONE_RE = re.compile(r'^\+?\d{9,15}$')
CARD_RE = re.compile(r'^\d{16}$')
CVV_RE = re.compile(r'^\d{3,4}$')
EXPIRY_RE = re.compile(r'^(0[1-9]|1[0-2])\/\d{2}$')


def validate_payment_data(method, amount, remaining, phone='', card_number='', card_expiry='', card_cvv=''):
    amount = Decimal(str(amount))
    if amount <= 0:
        raise ValidationError('Le montant doit être supérieur à zéro.')
    if amount > remaining:
        raise ValidationError(f'Le montant ne peut pas dépasser le reste à payer ({remaining} FCFA).')

    if method in MOBILE_METHODS:
        if not phone:
            raise ValidationError('Indiquez le numéro Mobile Money.')
        if not PHONE_RE.match(phone):
            raise ValidationError('Numéro de téléphone invalide (ex. +221771234567).')
    elif method == 'card':
        card_number = (card_number or '').replace(' ', '')
        if not CARD_RE.match(card_number):
            raise ValidationError('Numéro de carte invalide (16 chiffres).')
        if not EXPIRY_RE.match(card_expiry or ''):
            raise ValidationError("Date d'expiration invalide (MM/AA).")
        if not CVV_RE.match(card_cvv or ''):
            raise ValidationError('Code CVV invalide (3 ou 4 chiffres).')


def process_online_payment(invoice, method, amount, phone='', card_number='', card_expiry='', card_cvv=''):
    """Simule le traitement d'un paiement en ligne (démo sans API réelle)."""
    remaining = invoice.remaining_amount
    validate_payment_data(
        method, amount, remaining,
        phone=phone,
        card_number=card_number,
        card_expiry=card_expiry,
        card_cvv=card_cvv,
    )

    payment = Payment(
        invoice=invoice,
        payment_method=method,
        amount=Decimal(str(amount)),
        phone_number=phone if method in MOBILE_METHODS else '',
        status='pending',
    )
    if method == 'card' and card_number:
        payment.card_last_four = card_number.replace(' ', '')[-4:]

    payment.transaction_id = Payment.generate_transaction_id(method)
    payment.reference_number = payment.transaction_id
    payment.save()
    payment.complete()
    return payment
