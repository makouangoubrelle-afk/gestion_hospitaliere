from typing import List

from ninja import Router
from ninja.pagination import paginate

from audit.models import AuditLog
from audit.utils import log_audit, serialize_for_audit
from core.api.schemas import PatientInSchema, PatientOutSchema
from core.auth import jwt_auth
from core.pagination import SGHLPagination
from patients.models import Patient

router = Router(tags=['Patients'])


@router.get('/', response=List[PatientOutSchema], auth=jwt_auth)
@paginate(SGHLPagination)
def list_patients(request):
    return Patient.objects.all()


@router.post('/', response=PatientOutSchema, auth=jwt_auth)
def create_patient(request, payload: PatientInSchema):
    patient = Patient.objects.create(**payload.dict())
    log_audit(request, AuditLog.ActionType.CREATE, patient)
    return patient


@router.get('/{patient_id}', response=PatientOutSchema, auth=jwt_auth)
def get_patient(request, patient_id: int):
    return Patient.objects.get(pk=patient_id)
