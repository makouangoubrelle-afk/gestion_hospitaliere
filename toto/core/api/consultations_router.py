from typing import List

from ninja import Router
from ninja.pagination import paginate

from audit.models import AuditLog
from audit.utils import log_audit
from consultations.models import Consultation
from core.api.schemas import ConsultationInSchema, ConsultationOutSchema
from core.auth import jwt_auth
from core.pagination import SGHLPagination

router = Router(tags=['Consultations'])


@router.get('/', response=List[ConsultationOutSchema], auth=jwt_auth)
@paginate(SGHLPagination)
def list_consultations(request):
    return Consultation.objects.select_related('patient', 'medecin').all()


@router.post('/', response=ConsultationOutSchema, auth=jwt_auth)
def create_consultation(request, payload: ConsultationInSchema):
    data = payload.dict()
    patient_id = data.pop('patient_id')
    medecin_id = data.pop('medecin_id', None)
    consultation = Consultation.objects.create(
        patient_id=patient_id,
        medecin_id=medecin_id,
        **data,
    )
    log_audit(request, AuditLog.ActionType.CREATE, consultation)
    return consultation
