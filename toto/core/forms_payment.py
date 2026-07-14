from decimal import Decimal

from django import forms

from paiement.models import Payment


class InvoicePaymentForm(forms.Form):
    PAYMENT_METHODS = [
        ('card', 'Carte bancaire'),
        ('airtel_money', 'Airtel Mobile Money'),
        ('mtn_momo', 'MTN Mobile Money'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect,
        label='Mode de paiement',
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('1'),
        label='Montant (FCFA)',
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label='Numéro Mobile Money',
        widget=forms.TextInput(attrs={'placeholder': '+221771234567'}),
    )
    card_number = forms.CharField(
        max_length=19,
        required=False,
        label='Numéro de carte',
        widget=forms.TextInput(attrs={'placeholder': '4111 1111 1111 1111', 'autocomplete': 'cc-number'}),
    )
    card_expiry = forms.CharField(
        max_length=5,
        required=False,
        label="Expiration (MM/AA)",
        widget=forms.TextInput(attrs={'placeholder': '12/28', 'autocomplete': 'cc-exp'}),
    )
    card_cvv = forms.CharField(
        max_length=4,
        required=False,
        label='CVV',
        widget=forms.PasswordInput(attrs={'placeholder': '123', 'autocomplete': 'cc-csc'}),
    )

    def __init__(self, *args, invoice=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice = invoice
        if invoice and not self.is_bound:
            self.fields['amount'].initial = invoice.remaining_amount
        for field in self.fields.values():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.setdefault('class', 'input-field')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.invoice and amount > self.invoice.remaining_amount:
            raise forms.ValidationError(
                f'Le montant dépasse le reste à payer ({self.invoice.remaining_amount} FCFA).'
            )
        return amount
