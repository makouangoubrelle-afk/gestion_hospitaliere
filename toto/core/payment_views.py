from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from factures.models import Invoice
from paiement.services import process_online_payment

from .forms_payment import InvoicePaymentForm


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('patient', 'consultation').prefetch_related('items', 'payments'),
        pk=pk,
    )
    return render(request, 'core/facture_detail.html', {'invoice': invoice})


@login_required
def invoice_pay(request, invoice_id):
    invoice = get_object_or_404(Invoice.objects.select_related('patient'), pk=invoice_id)

    if invoice.status in ('paid', 'cancelled'):
        messages.warning(request, 'Cette facture est déjà soldée ou annulée.')
        return redirect('facture_detail', pk=invoice.pk)

    if invoice.remaining_amount <= 0:
        messages.info(request, 'Aucun montant restant à payer.')
        return redirect('facture_detail', pk=invoice.pk)

    form = InvoicePaymentForm(request.POST or None, invoice=invoice)

    if request.method == 'POST' and form.is_valid():
        try:
            payment = process_online_payment(
                invoice=invoice,
                method=form.cleaned_data['payment_method'],
                amount=form.cleaned_data['amount'],
                phone=form.cleaned_data.get('phone_number', ''),
                card_number=form.cleaned_data.get('card_number', ''),
                card_expiry=form.cleaned_data.get('card_expiry', ''),
                card_cvv=form.cleaned_data.get('card_cvv', ''),
            )
            label = dict(InvoicePaymentForm.PAYMENT_METHODS).get(payment.payment_method, '')
            messages.success(
                request,
                f'Paiement confirmé via {label}. Référence : {payment.transaction_id}',
            )
            return redirect('facture_detail', pk=invoice.pk)
        except ValidationError as exc:
            messages.error(request, exc.messages[0] if getattr(exc, 'messages', None) else str(exc))

    return render(request, 'core/payer_facture.html', {
        'invoice': invoice,
        'form': form,
    })
