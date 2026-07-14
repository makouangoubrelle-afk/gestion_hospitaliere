from typing import List

from ninja import Router
from ninja.pagination import paginate

from core.api.schemas import MedecinOutSchema
from core.auth import jwt_auth
from core.pagination import SGHLPagination
from medecins.models import Medecin

router = Router(tags=['Médecins'])


@router.get('/', response=List[MedecinOutSchema], auth=jwt_auth)
@paginate(SGHLPagination)
def list_medecins(request):
    return Medecin.objects.filter(status='active')
