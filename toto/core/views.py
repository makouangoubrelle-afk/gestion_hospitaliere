from decimal import Decimal
import json

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from core.forms import CustomUserCreationForm
from core.models import PlanningGarde, RendezVous
from core.redirects import get_role_home_url
from accounts.models import Role
from patients.models import Patient
from geolocalisation.models import SiteLocalise
from infirmiers.models import Infirmier
from medecins.models import Medecin
from consultations.models import Consultation
from factures.models import Invoice
from factures.pdf import generate_invoice_pdf
from paiement.models import Payment
from services.models import Service
from hospitalisation.models import Hospitalisation, Lit
from laboratoire.models import CommandeLabo
from laboratoire.pdf import generate_labo_report_pdf
from organisation.models import FileAttente, SalleAttente, SalleUrgence
from pharmacie.models import Medicament, Prescription
from secretaires.models import Secretaire


def home(request):
    if request.user.is_authenticated and request.path == '/':
        profile = getattr(request.user, 'profile', None)
        if profile and profile.role != Role.PATIENT:
            return redirect(get_role_home_url(request.user))
    return render(request, 'core/home.html')


def _login_redirect_url(request, user=None):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    if user and user.is_authenticated:
        return get_role_home_url(user)
    return '/'


def user_login(request):
    if request.user.is_authenticated:
        return redirect(_login_redirect_url(request, request.user))

    form = AuthenticationForm(request, data=request.POST or None)
    form.fields['username'].label = "Nom d'utilisateur"
    form.fields['password'].label = 'Mot de passe'

    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.get_user())
        return redirect(_login_redirect_url(request, form.get_user()))

    for field in form.fields.values():
        field.widget.attrs.setdefault('class', 'input-field')

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    lits_total = Lit.objects.count() or 1
    lits_occupes = Lit.objects.filter(statut=Lit.Statut.OCCUPE).count()
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    recettes = Invoice.objects.filter(
        issue_date__gte=debut_mois.date(),
        status__in=['paid', 'partial'],
    ).aggregate(total=Sum('paid_amount'))['total'] or Decimal('0')
    kpis = {
        'patients_actifs': Patient.objects.filter(status='active').count(),
        'taux_occupation': round((lits_occupes / lits_total) * 100, 1),
        'recettes_mois': recettes,
        'examens_en_attente': CommandeLabo.objects.exclude(
            statut__in=['validee', 'publiee', 'annulee']
        ).count(),
        'lits_disponibles': Lit.objects.filter(statut=Lit.Statut.DISPONIBLE).count(),
        'consultations_du_jour': Consultation.objects.filter(
            appointment_date__date=timezone.now().date()
        ).count(),
    }
    return render(request, 'core/dashboard.html', {'kpis': kpis})


@login_required
def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'core/patients.html', {'patients': patients})


@login_required
def medecins_list(request):
    medecins = Medecin.objects.all()
    return render(request, 'core/medecins.html', {'medecins': medecins})


@login_required
def infirmiers_list(request):
    infirmiers = Infirmier.objects.all()
    return render(request, 'core/infirmiers.html', {'infirmiers': infirmiers})


@login_required
def geolocalisation_list(request):
    sites = SiteLocalise.objects.filter(is_active=True)
    sites_map = [
        {
            'id': s.pk,
            'nom': s.nom,
            'type': s.get_type_lieu_display(),
            'adresse': s.adresse,
            'ville': s.ville,
            'telephone': s.telephone,
            'lat': float(s.latitude),
            'lng': float(s.longitude),
        }
        for s in sites
    ]
    return render(request, 'core/geolocalisation.html', {
        'sites': sites,
        'sites_json': json.dumps(sites_map),
    })


@login_required
def secretaires_list(request):
    secretaires = Secretaire.objects.all()
    return render(request, 'core/secretaires.html', {'secretaires': secretaires})


@login_required
def salles_urgence_list(request):
    salles = SalleUrgence.objects.select_related('patient', 'medecin').all()
    return render(request, 'core/salles_urgence.html', {'salles': salles})


@login_required
def salles_attente_list(request):
    salles = SalleAttente.objects.filter(is_active=True)
    files = FileAttente.objects.select_related('patient', 'salle_attente').filter(
        statut=FileAttente.Statut.EN_ATTENTE,
    )
    return render(request, 'core/salles_attente.html', {
        'salles': salles,
        'files': files,
    })


@login_required
def agenda_list(request):
    now = timezone.now()
    rendez_vous = RendezVous.objects.select_related('patient', 'medecin').filter(
        date_rdv__gte=now - timezone.timedelta(days=1),
    ).order_by('date_rdv')[:80]
    consultations = Consultation.objects.select_related('patient', 'medecin').filter(
        appointment_date__gte=now - timezone.timedelta(days=1),
    ).order_by('appointment_date')[:80]
    gardes = PlanningGarde.objects.select_related('medecin', 'service').filter(
        date_fin__gte=now,
    ).order_by('date_debut')[:30]
    return render(request, 'core/agenda.html', {
        'rendez_vous': rendez_vous,
        'consultations': consultations,
        'gardes': gardes,
    })


@login_required
def consultations_list(request):
    consultations = Consultation.objects.select_related('patient', 'medecin').all()
    return render(request, 'core/consultations.html', {'consultations': consultations})


@login_required
def invoices_list(request):
    invoices = Invoice.objects.select_related('patient', 'consultation').all()
    return render(request, 'core/factures.html', {'invoices': invoices})


@login_required
def payments_list(request):
    payments = Payment.objects.select_related('invoice__patient').all()
    return render(request, 'core/paiement.html', {'payments': payments})


@login_required
def services_list(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})


@login_required
def hospitalisation_list(request):
    hospitalisations = Hospitalisation.objects.select_related('patient', 'lit', 'medecin_referent').all()
    lits = Lit.objects.select_related('chambre__service__batiment').all()
    return render(request, 'core/hospitalisation.html', {
        'hospitalisations': hospitalisations,
        'lits': lits,
    })


@login_required
def laboratoire_list(request):
    commandes = CommandeLabo.objects.select_related('patient', 'type_examen', 'medecin_prescripteur').all()
    return render(request, 'core/laboratoire.html', {'commandes': commandes})


@login_required
def pharmacie_list(request):
    medicaments = Medicament.objects.all()
    prescriptions = Prescription.objects.select_related('consultation', 'medicament').all()
    return render(request, 'core/pharmacie.html', {
        'medicaments': medicaments,
        'prescriptions': prescriptions,
    })


@login_required
def invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice.objects.prefetch_related('items'), pk=invoice_id)
    pdf_bytes = generate_invoice_pdf(invoice)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="facture_{invoice.invoice_number}.pdf"'
    return response


@login_required
def labo_pdf(request, commande_id):
    commande = get_object_or_404(
        CommandeLabo.objects.select_related('patient', 'type_examen', 'medecin_prescripteur'),
        pk=commande_id,
    )
    if not hasattr(commande, 'resultat'):
        return HttpResponse('Aucun résultat disponible', status=404)
    pdf_bytes = generate_labo_report_pdf(commande, commande.resultat)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="rapport_{commande.numero_commande}.pdf"'
    return response
