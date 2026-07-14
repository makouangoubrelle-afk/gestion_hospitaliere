from typing import List

from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from audit.models import AuditLog
from audit.utils import log_audit
from core.api.schemas import PrescriptionInSchema, RendezVousInSchema
from core.auth import jwt_auth
from core.pagination import SGHLPagination
from core.models import RendezVous
from pharmacie.models import Medicament, Prescription

router = Router(tags=['Pharmacie & RDV'])


@router.get('/medicaments', response=List[dict], auth=jwt_auth)
@paginate(SGHLPagination)
def list_medicaments(request):
    return [
        {
            'id': m.id,
            'nom': m.nom,
            'code': m.code,
            'stock_total': m.stock_total,
            'seuil_alerte': m.seuil_alerte,
            'alerte_rupture': m.stock_total <= m.seuil_alerte,
        }
        for m in Medicament.objects.filter(is_active=True)
    ]


@router.post('/prescriptions', response=dict, auth=jwt_auth)
def create_prescription(request, payload: PrescriptionInSchema):
    prescription = Prescription.objects.create(**payload.dict())
    log_audit(request, AuditLog.ActionType.CREATE, prescription)
    return {'id': prescription.id, 'statut': prescription.statut}


@router.post('/prescriptions/{prescription_id}/valider', response=dict, auth=jwt_auth)
def valider_prescription(request, prescription_id: int):
    prescription = Prescription.objects.get(pk=prescription_id)
    try:
        prescription.valider()
    except Exception as exc:
        raise HttpError(400, str(exc))
    log_audit(request, AuditLog.ActionType.VALIDATE, prescription)
    return {'id': prescription.id, 'statut': prescription.statut}


@router.get('/rendez-vous', response=List[dict], auth=jwt_auth)
@paginate(SGHLPagination)
def list_rdv(request):
    return [
        {
            'id': r.id,
            'patient': r.patient.full_name,
            'medecin': r.medecin.full_name,
            'date_rdv': r.date_rdv.isoformat(),
            'statut': r.statut,
        }
        for r in RendezVous.objects.select_related('patient', 'medecin').all()
    ]


@router.post('/rendez-vous', response=dict, auth=jwt_auth)
def create_rdv(request, payload: RendezVousInSchema):
    rdv = RendezVous.objects.create(**payload.dict())
    log_audit(request, AuditLog.ActionType.CREATE, rdv)
    return {'id': rdv.id, 'statut': rdv.statut}
