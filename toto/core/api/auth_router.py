from datetime import datetime
from decimal import Decimal

from django.contrib.auth import authenticate
from django.db import connection
from django.db.models import Sum
from django.utils import timezone
from ninja import Router
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import LoginJournal, Role
from audit.models import AuditLog
from audit.utils import get_client_ip, log_audit
from consultations.models import Consultation
from core.api.schemas import DashboardSchema, LoginSchema, MessageSchema, SanteSchema, TokenSchema, UserOutSchema
from core.auth import jwt_auth
from factures.models import Invoice
from hospitalisation.models import Hospitalisation, Lit
from laboratoire.models import CommandeLabo
from patients.models import Patient

router = Router(tags=['Authentification & Pilotage'])


@router.post('/auth/login', response={200: TokenSchema, 401: MessageSchema}, auth=None)
def login(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        return 401, {'detail': 'Identifiants invalides'}
    refresh = RefreshToken.for_user(user)
    LoginJournal.objects.create(
        user=user,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        success=True,
    )
    request.user = user
    log_audit(request, AuditLog.ActionType.LOGIN, user, description='Connexion JWT réussie')
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}


@router.get('/auth/me', response=UserOutSchema, auth=jwt_auth)
def me(request):
    profile = getattr(request.user, 'profile', None)
    role = profile.role if profile else Role.PATIENT
    return {
        'id': request.user.id,
        'username': request.user.username,
        'role': role,
        'email': request.user.email,
    }


@router.get('/sante/', response=SanteSchema, auth=None)
def sante(request):
    db_ok = 'ok'
    try:
        connection.ensure_connection()
    except Exception:
        db_ok = 'error'
    return {
        'status': 'healthy' if db_ok == 'ok' else 'degraded',
        'version': '1.0.0',
        'database': db_ok,
        'timestamp': timezone.now(),
    }


@router.get('/dashboard/kpis', response=DashboardSchema, auth=jwt_auth)
def dashboard_kpis(request):
    lits_total = Lit.objects.count() or 1
    lits_occupes = Lit.objects.filter(statut=Lit.Statut.OCCUPE).count()
    taux = round((lits_occupes / lits_total) * 100, 2)
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    recettes = Invoice.objects.filter(
        issue_date__gte=debut_mois.date(),
        status__in=['paid', 'partial'],
    ).aggregate(total=Sum('paid_amount'))['total'] or Decimal('0')
    return {
        'patients_actifs': Patient.objects.filter(status='active').count(),
        'taux_occupation': taux,
        'recettes_mois': recettes,
        'examens_en_attente': CommandeLabo.objects.exclude(
            statut__in=[CommandeLabo.Statut.VALIDEE, CommandeLabo.Statut.PUBLIEE, CommandeLabo.Statut.ANNULEE]
        ).count(),
        'lits_disponibles': Lit.objects.filter(statut=Lit.Statut.DISPONIBLE).count(),
        'lits_total': lits_total,
        'consultations_du_jour': Consultation.objects.filter(
            appointment_date__date=timezone.now().date()
        ).count(),
    }
