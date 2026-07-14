"""
Django Ninja API SGHL - versionnée /api/v1/
"""
from ninja import NinjaAPI
from django.http import JsonResponse

from core.exceptions import CHLABAPIException
from core.api.auth_router import router as auth_router
from core.api.patients_router import router as patients_router
from core.api.medecins_router import router as medecins_router
from core.api.consultations_router import router as consultations_router
from core.api.hospitalisation_router import router as hospitalisation_router
from core.api.factures_router import router as factures_router
from core.api.laboratoire_router import router as laboratoire_router
from core.api.pharmacie_router import router as pharmacie_router

api = NinjaAPI(
    title='SGHL - Système de Gestion Hospitalière et de Laboratoire',
    version='1.0.0',
    description='API REST conforme au cahier des charges GI3 2025-2026',
    urls_namespace='api-v1',
    docs_url=None,
    openapi_url=None,
)

api.add_router('', auth_router)
api.add_router('/patients', patients_router)
api.add_router('/medecins', medecins_router)
api.add_router('/consultations', consultations_router)
api.add_router('/hospitalisation', hospitalisation_router)
api.add_router('/laboratoire', laboratoire_router)
api.add_router('/pharmacie', pharmacie_router)
api.add_router('/factures', factures_router)


@api.exception_handler(CHLABAPIException)
def handle_chlab_exceptions(request, exc):
    return JsonResponse({
        'error': {
            'code': exc.code,
            'message': exc.message,
            'status': exc.status_code,
        }
    }, status=exc.status_code)


@api.exception_handler(Exception)
def handle_generic_exceptions(request, exc):
    return JsonResponse({
        'error': {
            'code': 'INTERNAL_SERVER_ERROR',
            'message': 'Une erreur interne est survenue',
            'status': 500,
        }
    }, status=500)
