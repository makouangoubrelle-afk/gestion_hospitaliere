from django import forms

from consultations.models import Consultation
from core.models import RendezVous
from factures.models import Invoice
from geolocalisation.models import SiteLocalise
from infirmiers.models import Infirmier
from medecins.models import Medecin
from organisation.models import FileAttente, SalleAttente, SalleUrgence
from patients.models import Patient
from pharmacie.models import Medicament
from secretaires.models import Secretaire
from services.models import Service


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                continue
            field.widget.attrs.setdefault('class', 'input-field')


class PatientForm(StyledModelForm):
    class Meta:
        model = Patient
        fields = [
            'patient_id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'email', 'phone', 'address', 'city', 'postal_code', 'country',
            'blood_type', 'allergies', 'medical_history', 'status',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class MedecinForm(StyledModelForm):
    class Meta:
        model = Medecin
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'license_number',
            'specialty', 'department', 'years_experience', 'status',
        ]


class InfirmierForm(StyledModelForm):
    class Meta:
        model = Infirmier
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'matricule',
            'service', 'grade', 'unite', 'shift', 'years_experience', 'status',
        ]


class SecretaireForm(StyledModelForm):
    class Meta:
        model = Secretaire
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'matricule',
            'bureau', 'service_accueil', 'horaires', 'status',
        ]


class SalleUrgenceForm(StyledModelForm):
    class Meta:
        model = SalleUrgence
        fields = ['code', 'nom', 'capacite', 'statut', 'patient', 'medecin', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 2})}


class SalleAttenteForm(StyledModelForm):
    class Meta:
        model = SalleAttente
        fields = ['code', 'nom', 'capacite', 'zone', 'is_active']


class FileAttenteForm(StyledModelForm):
    class Meta:
        model = FileAttente
        fields = ['salle_attente', 'patient', 'motif', 'priorite', 'statut']


class RendezVousForm(StyledModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'medecin', 'date_rdv', 'motif', 'statut']
        widgets = {
            'date_rdv': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motif': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.date_rdv:
            self.initial['date_rdv'] = self.instance.date_rdv.strftime('%Y-%m-%dT%H:%M')


class SiteLocaliseForm(StyledModelForm):
    class Meta:
        model = SiteLocalise
        fields = [
            'nom', 'type_lieu', 'adresse', 'ville', 'latitude', 'longitude',
            'telephone', 'description', 'is_active',
        ]
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'latitude': forms.NumberInput(attrs={'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'step': 'any'}),
        }


class ConsultationForm(StyledModelForm):
    class Meta:
        model = Consultation
        fields = [
            'patient', 'medecin', 'visit_type', 'appointment_date', 'duration_minutes',
            'chief_complaint', 'diagnosis', 'cim10_code', 'treatment_plan', 'notes', 'status',
        ]
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'chief_complaint': forms.Textarea(attrs={'rows': 2}),
            'diagnosis': forms.Textarea(attrs={'rows': 2}),
            'treatment_plan': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.appointment_date:
            self.initial['appointment_date'] = self.instance.appointment_date.strftime('%Y-%m-%dT%H:%M')


class ServiceForm(StyledModelForm):
    class Meta:
        model = Service
        fields = [
            'name', 'code', 'description', 'phone', 'email', 'is_active',
            'monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours',
            'friday_hours', 'saturday_hours', 'sunday_hours',
        ]
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class MedicamentForm(StyledModelForm):
    class Meta:
        model = Medicament
        fields = ['nom', 'code', 'forme', 'dosage', 'seuil_alerte', 'is_active']


class InvoiceForm(StyledModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_number', 'patient', 'consultation', 'due_date', 'subtotal', 'tax',
            'total_amount', 'paid_amount', 'status', 'assurance_nom', 'assurance_numero',
            'montant_assurance', 'montant_patient', 'description', 'notes',
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
