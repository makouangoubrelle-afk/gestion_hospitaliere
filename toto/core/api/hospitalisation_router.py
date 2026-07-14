from typing import List

from ninja import Router
from ninja.pagination import paginate

from audit.models import AuditLog
from audit.utils import log_audit
from core.api.schemas import HospitalisationInSchema, HospitalisationOutSchema
from core.auth import jwt_auth
from core.pagination import SGHLPagination
from hospitalisation.models import Hospitalisation, Lit

router = Router(tags=['Hospitalisation'])


@router.get('/', response=List[HospitalisationOutSchema], auth=jwt_auth)
@paginate(SGHLPagination)
def list_hospitalisations(request):
    return Hospitalisation.objects.select_related('patient', 'lit', 'medecin_referent').all()


@router.post('/', response=HospitalisationOutSchema, auth=jwt_auth)
def create_hospitalisation(request, payload: HospitalisationInSchema):
    lit = Lit.objects.get(pk=payload.lit_id)
    if lit.statut != Lit.Statut.DISPONIBLE:
        from ninja.errors import HttpError
        raise HttpError(400, 'Lit non disponible — règle métier: 1 lit = 1 patient maximum')
    hospitalisation = Hospitalisation(
        patient_id=payload.patient_id,
        lit=lit,
        medecin_referent_id=payload.medecin_referent_id,
        date_sortie_prevue=payload.date_sortie_prevue,
        motif=payload.motif,
    )
    hospitalisation.save()
    log_audit(request, AuditLog.ActionType.CREATE, hospitalisation)
    return hospitalisation
