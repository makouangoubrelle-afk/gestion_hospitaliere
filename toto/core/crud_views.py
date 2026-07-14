from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import admin_required
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

from .forms_admin import (
    ConsultationForm,
    FileAttenteForm,
    InfirmierForm,
    InvoiceForm,
    MedecinForm,
    MedicamentForm,
    PatientForm,
    RendezVousForm,
    SalleAttenteForm,
    SalleUrgenceForm,
    SecretaireForm,
    ServiceForm,
    SiteLocaliseForm,
)


def _handle_form(request, form, success_message, redirect_url):
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect(redirect_url)
    return None


def _delete_object(request, obj, redirect_url, label):
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f'{label} supprimé(e) avec succès.')
        return redirect(redirect_url)
    return render(request, 'core/confirm_delete.html', {'object_label': label, 'object': obj})


# --- Patients ---
@admin_required
def patient_create(request):
    form = PatientForm(request.POST or None)
    response = _handle_form(request, form, 'Patient ajouté avec succès.', 'patients')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un patient', 'form': form, 'cancel_url': 'patients',
    })


@admin_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    response = _handle_form(request, form, 'Patient modifié avec succès.', 'patients')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {patient.full_name}', 'form': form, 'cancel_url': 'patients',
    })


@admin_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return _delete_object(request, patient, 'patients', f'Patient {patient.full_name}')


# --- Médecins ---
@admin_required
def medecin_create(request):
    form = MedecinForm(request.POST or None)
    response = _handle_form(request, form, 'Médecin ajouté avec succès.', 'medecins')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un médecin', 'form': form, 'cancel_url': 'medecins',
    })


@admin_required
def medecin_update(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    form = MedecinForm(request.POST or None, instance=medecin)
    response = _handle_form(request, form, 'Médecin modifié avec succès.', 'medecins')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier Dr. {medecin.last_name}', 'form': form, 'cancel_url': 'medecins',
    })


@admin_required
def medecin_delete(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    return _delete_object(request, medecin, 'medecins', f'Médecin {medecin.full_name}')


# --- Infirmiers ---
@admin_required
def infirmier_create(request):
    form = InfirmierForm(request.POST or None)
    response = _handle_form(request, form, 'Infirmier(ère) ajouté(e) avec succès.', 'infirmiers')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un(e) infirmier(ère)', 'form': form, 'cancel_url': 'infirmiers',
    })


@admin_required
def infirmier_update(request, pk):
    infirmier = get_object_or_404(Infirmier, pk=pk)
    form = InfirmierForm(request.POST or None, instance=infirmier)
    response = _handle_form(request, form, 'Infirmier(ère) modifié(e) avec succès.', 'infirmiers')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {infirmier.full_name}', 'form': form, 'cancel_url': 'infirmiers',
    })


@admin_required
def infirmier_delete(request, pk):
    infirmier = get_object_or_404(Infirmier, pk=pk)
    return _delete_object(request, infirmier, 'infirmiers', f'Infirmier(ère) {infirmier.full_name}')


# --- Géolocalisation ---
@admin_required
def site_create(request):
    form = SiteLocaliseForm(request.POST or None)
    response = _handle_form(request, form, 'Site ajouté avec succès.', 'geolocalisation')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un site géolocalisé', 'form': form, 'cancel_url': 'geolocalisation',
    })


@admin_required
def site_update(request, pk):
    site = get_object_or_404(SiteLocalise, pk=pk)
    form = SiteLocaliseForm(request.POST or None, instance=site)
    response = _handle_form(request, form, 'Site modifié avec succès.', 'geolocalisation')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {site.nom}', 'form': form, 'cancel_url': 'geolocalisation',
    })


@admin_required
def site_delete(request, pk):
    site = get_object_or_404(SiteLocalise, pk=pk)
    return _delete_object(request, site, 'geolocalisation', f'Site {site.nom}')


# --- Consultations ---
@admin_required
def consultation_create(request):
    form = ConsultationForm(request.POST or None)
    response = _handle_form(request, form, 'Consultation ajoutée avec succès.', 'consultations')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter une consultation', 'form': form, 'cancel_url': 'consultations',
    })


@admin_required
def consultation_update(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    form = ConsultationForm(request.POST or None, instance=consultation)
    response = _handle_form(request, form, 'Consultation modifiée avec succès.', 'consultations')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Modifier la consultation', 'form': form, 'cancel_url': 'consultations',
    })


@admin_required
def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return _delete_object(request, consultation, 'consultations', 'Consultation')


# --- Services ---
@admin_required
def service_create(request):
    form = ServiceForm(request.POST or None)
    response = _handle_form(request, form, 'Service ajouté avec succès.', 'services')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un service', 'form': form, 'cancel_url': 'services',
    })


@admin_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, instance=service)
    response = _handle_form(request, form, 'Service modifié avec succès.', 'services')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {service.name}', 'form': form, 'cancel_url': 'services',
    })


@admin_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return _delete_object(request, service, 'services', f'Service {service.name}')


# --- Médicaments ---
@admin_required
def medicament_create(request):
    form = MedicamentForm(request.POST or None)
    response = _handle_form(request, form, 'Médicament ajouté avec succès.', 'pharmacie')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un médicament', 'form': form, 'cancel_url': 'pharmacie',
    })


@admin_required
def medicament_update(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    form = MedicamentForm(request.POST or None, instance=medicament)
    response = _handle_form(request, form, 'Médicament modifié avec succès.', 'pharmacie')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {medicament.nom}', 'form': form, 'cancel_url': 'pharmacie',
    })


@admin_required
def medicament_delete(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    return _delete_object(request, medicament, 'pharmacie', f'Médicament {medicament.nom}')


# --- Factures ---
@admin_required
def invoice_create(request):
    form = InvoiceForm(request.POST or None)
    response = _handle_form(request, form, 'Facture ajoutée avec succès.', 'factures')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter une facture', 'form': form, 'cancel_url': 'factures',
    })


@admin_required
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    form = InvoiceForm(request.POST or None, instance=invoice)
    response = _handle_form(request, form, 'Facture modifiée avec succès.', 'factures')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier facture {invoice.invoice_number}', 'form': form, 'cancel_url': 'factures',
    })


@admin_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return _delete_object(request, invoice, 'factures', f'Facture {invoice.invoice_number}')


# --- Secrétaires ---
@admin_required
def secretaire_create(request):
    form = SecretaireForm(request.POST or None)
    response = _handle_form(request, form, 'Secrétaire ajouté(e) avec succès.', 'secretaires')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un(e) secrétaire', 'form': form, 'cancel_url': 'secretaires',
    })


@admin_required
def secretaire_update(request, pk):
    secretaire = get_object_or_404(Secretaire, pk=pk)
    form = SecretaireForm(request.POST or None, instance=secretaire)
    response = _handle_form(request, form, 'Secrétaire modifié(e) avec succès.', 'secretaires')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {secretaire.full_name}', 'form': form, 'cancel_url': 'secretaires',
    })


@admin_required
def secretaire_delete(request, pk):
    secretaire = get_object_or_404(Secretaire, pk=pk)
    return _delete_object(request, secretaire, 'secretaires', f'Secrétaire {secretaire.full_name}')


# --- Salles d'urgence ---
@admin_required
def salle_urgence_create(request):
    form = SalleUrgenceForm(request.POST or None)
    response = _handle_form(request, form, "Salle d'urgence ajoutée.", 'salles_urgence')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': "Ajouter une salle d'urgence", 'form': form, 'cancel_url': 'salles_urgence',
    })


@admin_required
def salle_urgence_update(request, pk):
    salle = get_object_or_404(SalleUrgence, pk=pk)
    form = SalleUrgenceForm(request.POST or None, instance=salle)
    response = _handle_form(request, form, "Salle d'urgence modifiée.", 'salles_urgence')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {salle.nom}', 'form': form, 'cancel_url': 'salles_urgence',
    })


@admin_required
def salle_urgence_delete(request, pk):
    salle = get_object_or_404(SalleUrgence, pk=pk)
    return _delete_object(request, salle, 'salles_urgence', f"Salle {salle.nom}")


# --- Salles d'attente ---
@admin_required
def salle_attente_create(request):
    form = SalleAttenteForm(request.POST or None)
    response = _handle_form(request, form, "Salle d'attente ajoutée.", 'salles_attente')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': "Ajouter une salle d'attente", 'form': form, 'cancel_url': 'salles_attente',
    })


@admin_required
def salle_attente_update(request, pk):
    salle = get_object_or_404(SalleAttente, pk=pk)
    form = SalleAttenteForm(request.POST or None, instance=salle)
    response = _handle_form(request, form, "Salle d'attente modifiée.", 'salles_attente')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': f'Modifier {salle.nom}', 'form': form, 'cancel_url': 'salles_attente',
    })


@admin_required
def salle_attente_delete(request, pk):
    salle = get_object_or_404(SalleAttente, pk=pk)
    return _delete_object(request, salle, 'salles_attente', f"Salle {salle.nom}")


# --- File d'attente ---
@admin_required
def file_attente_create(request):
    form = FileAttenteForm(request.POST or None)
    response = _handle_form(request, form, 'Patient ajouté à la file.', 'salles_attente')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': "Ajouter un patient en attente", 'form': form, 'cancel_url': 'salles_attente',
    })


@admin_required
def file_attente_update(request, pk):
    entree = get_object_or_404(FileAttente, pk=pk)
    form = FileAttenteForm(request.POST or None, instance=entree)
    response = _handle_form(request, form, 'File mise à jour.', 'salles_attente')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Modifier la file d\'attente', 'form': form, 'cancel_url': 'salles_attente',
    })


@admin_required
def file_attente_delete(request, pk):
    entree = get_object_or_404(FileAttente, pk=pk)
    return _delete_object(request, entree, 'salles_attente', f'Entrée file {entree.patient}')


# --- Agenda (rendez-vous) ---
@admin_required
def rendez_vous_create(request):
    form = RendezVousForm(request.POST or None)
    response = _handle_form(request, form, 'Rendez-vous ajouté.', 'agenda')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Ajouter un rendez-vous', 'form': form, 'cancel_url': 'agenda',
    })


@admin_required
def rendez_vous_update(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)
    form = RendezVousForm(request.POST or None, instance=rdv)
    response = _handle_form(request, form, 'Rendez-vous modifié.', 'agenda')
    if response:
        return response
    return render(request, 'core/form_page.html', {
        'title': 'Modifier le rendez-vous', 'form': form, 'cancel_url': 'agenda',
    })


@admin_required
def rendez_vous_delete(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)
    return _delete_object(request, rdv, 'agenda', 'Rendez-vous')
