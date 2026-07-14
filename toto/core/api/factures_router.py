from django.http import HttpResponse
from ninja import Router
from ninja.errors import HttpError

from core.auth import jwt_auth
from factures.models import Invoice
from factures.pdf import generate_invoice_pdf

router = Router(tags=['Facturation'])


@router.get('/{invoice_id}/pdf', auth=jwt_auth)
def download_invoice_pdf(request, invoice_id: int):
    try:
        invoice = Invoice.objects.select_related('patient').prefetch_related('items').get(pk=invoice_id)
    except Invoice.DoesNotExist:
        raise HttpError(404, 'Facture introuvable')
    pdf_bytes = generate_invoice_pdf(invoice)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{invoice.invoice_number}.pdf"'
    return response
