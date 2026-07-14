from io import BytesIO
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_invoice_pdf(invoice) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], textColor=colors.HexColor('#1d4ed8'))
    elements = [
        Paragraph('SGHL — Facture médicale', title_style),
        Spacer(1, 0.5 * cm),
        Paragraph(f'<b>N° facture :</b> {invoice.invoice_number}'),
        Paragraph(f'<b>Date :</b> {invoice.issue_date.strftime("%d/%m/%Y")}'),
        Paragraph(f'<b>Échéance :</b> {invoice.due_date.strftime("%d/%m/%Y")}'),
        Spacer(1, 0.5 * cm),
        Paragraph(f'<b>Patient :</b> {invoice.patient.full_name} ({invoice.patient.patient_id})'),
        Paragraph(f'<b>Adresse :</b> {invoice.patient.address}, {invoice.patient.city}'),
    ]

    if invoice.assurance_nom:
        elements.append(Paragraph(
            f'<b>Tiers payant :</b> {invoice.assurance_nom} — N° {invoice.assurance_numero or "N/A"}'
        ))

    elements.append(Spacer(1, 0.8 * cm))

    rows = [['Description', 'Qté', 'P.U. (FCFA)', 'Sous-total (FCFA)']]
    for item in invoice.items.all():
        rows.append([
            item.description,
            str(item.quantity),
            f'{item.unit_price:,.0f}',
            f'{item.subtotal:,.0f}',
        ])

    if len(rows) == 1:
        rows.append(['Actes médicaux', '1', f'{invoice.subtotal:,.0f}', f'{invoice.subtotal:,.0f}'])

    table = Table(rows, colWidths=[8 * cm, 2 * cm, 3 * cm, 3 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eef2ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.8 * cm))

    totals = [
        ['Sous-total', f'{invoice.subtotal:,.0f} FCFA'],
        ['TVA', f'{invoice.tax:,.0f} FCFA'],
        ['Total', f'{invoice.total_amount:,.0f} FCFA'],
        ['Payé', f'{invoice.paid_amount:,.0f} FCFA'],
        ['Reste dû', f'{invoice.remaining_amount:,.0f} FCFA'],
    ]
    if invoice.montant_assurance:
        totals.insert(3, ['Part assurance', f'{invoice.montant_assurance:,.0f} FCFA'])
        totals.insert(4, ['Part patient', f'{invoice.montant_patient:,.0f} FCFA'])

    total_table = Table(totals, colWidths=[10 * cm, 6 * cm])
    total_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph(
        '<i>Document généré électroniquement par SGHL — signature électronique simulée.</i>',
        styles['Normal'],
    ))

    doc.build(elements)
    return buffer.getvalue()
