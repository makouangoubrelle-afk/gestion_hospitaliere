from io import BytesIO

from django.core.files.base import ContentFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_labo_report_pdf(commande, resultat) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], textColor=colors.HexColor('#1d4ed8'))

    elements = [
        Paragraph('SGHL — Compte-rendu de laboratoire', title_style),
        Spacer(1, 0.5 * cm),
        Paragraph(f'<b>N° commande :</b> {commande.numero_commande}'),
        Paragraph(f'<b>Patient :</b> {commande.patient.full_name} ({commande.patient.patient_id})'),
        Paragraph(f'<b>Examen :</b> {commande.type_examen.nom} ({commande.type_examen.code})'),
        Paragraph(f'<b>Prescripteur :</b> {commande.medecin_prescripteur.full_name}'),
        Spacer(1, 0.8 * cm),
    ]

    rows = [
        ['Paramètre', 'Résultat', 'Unité', 'Valeurs de référence'],
        [commande.type_examen.nom, resultat.valeur, resultat.unite or '-', resultat.reference or '-'],
    ]
    table = Table(rows, colWidths=[5 * cm, 4 * cm, 3 * cm, 4 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eef2ff')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 1 * cm))

    if resultat.valide:
        validateur = resultat.valide_par.get_full_name() or resultat.valide_par.username if resultat.valide_par else 'Biologiste'
        date_val = resultat.date_validation.strftime('%d/%m/%Y %H:%M') if resultat.date_validation else '-'
        elements.append(Paragraph(f'<b>Validé par :</b> {validateur} le {date_val}'))
        elements.append(Paragraph('<i>Résultat validé — document immuable — signature électronique simulée.</i>'))

    doc.build(elements)
    return buffer.getvalue()


def save_labo_report_pdf(resultat) -> str:
    pdf_bytes = generate_labo_report_pdf(resultat.commande, resultat)
    filename = f'rapport_{resultat.commande.numero_commande}.pdf'
    resultat.rapport_pdf.save(filename, ContentFile(pdf_bytes), save=True)
    return resultat.rapport_pdf.url
