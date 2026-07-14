import pytest
from datetime import date
from decimal import Decimal

from factures.models import Invoice, InvoiceItem
from factures.pdf import generate_invoice_pdf
from laboratoire.pdf import generate_labo_report_pdf
from patients.models import Patient


@pytest.mark.django_db
def test_generate_invoice_pdf():
    patient = Patient.objects.create(
        first_name='Test', last_name='Patient', date_of_birth='1990-01-01',
        gender='M', email='test@test.sn', phone='+221771111111',
        address='Dakar', city='Dakar', postal_code='10000', patient_id='TEST-001',
    )
    invoice = Invoice.objects.create(
        patient=patient,
        invoice_number='TEST-FAC-001',
        due_date=date(2026, 12, 31),
        subtotal=Decimal('10000'),
        total_amount=Decimal('10000'),
    )
    InvoiceItem.objects.create(
        invoice=invoice, description='Consultation', quantity=1,
        unit_price=Decimal('10000'), subtotal=Decimal('10000'),
    )
    pdf = generate_invoice_pdf(invoice)
    assert pdf[:4] == b'%PDF'
    assert len(pdf) > 500


@pytest.mark.django_db
def test_generate_labo_pdf_without_result():
    from laboratoire.models import CommandeLabo, ResultatLabo, TypeExamen
    from medecins.models import Medecin

    patient = Patient.objects.create(
        first_name='Lab', last_name='Patient', date_of_birth='1988-05-05',
        gender='F', email='lab@test.sn', phone='+221772222222',
        address='Dakar', city='Dakar', postal_code='10000', patient_id='TEST-002',
    )
    medecin = Medecin.objects.create(
        first_name='Dr', last_name='Test', email='dr@test.sn', phone='+221773333333',
        license_number='LIC-TEST', specialty='general', department='Général', years_experience=5,
    )
    from consultations.models import Consultation
    from django.utils import timezone
    consultation = Consultation.objects.create(
        patient=patient, medecin=medecin, visit_type='outpatient',
        appointment_date=timezone.now(), chief_complaint='Test',
    )
    examen = TypeExamen.objects.create(code='TST', nom='Test sanguin', prix=Decimal('5000'))
    commande = CommandeLabo.objects.create(
        patient=patient, consultation=consultation, medecin_prescripteur=medecin,
        type_examen=examen, numero_commande='LAB-TEST-001',
    )
    resultat = ResultatLabo.objects.create(commande=commande, valeur='12.5', unite='g/dL', reference='10-15')
    pdf = generate_labo_report_pdf(commande, resultat)
    assert pdf[:4] == b'%PDF'
