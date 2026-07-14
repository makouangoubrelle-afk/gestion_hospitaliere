from typing import List

from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from audit.models import AuditLog
from audit.utils import log_audit, serialize_for_audit
from core.api.schemas import CommandeLaboInSchema, ResultatLaboInSchema
from core.auth import jwt_auth
from core.pagination import SGHLPagination
from laboratoire.models import CommandeLabo, ResultatLabo
from laboratoire.pdf import generate_labo_report_pdf, save_labo_report_pdf

router = Router(tags=['Laboratoire (LIS)'])


@router.get('/commandes', response=List[dict], auth=jwt_auth)
@paginate(SGHLPagination)
def list_commandes(request):
    return [
        {
            'id': c.id,
            'numero_commande': c.numero_commande,
            'patient': c.patient.full_name,
            'statut': c.statut,
            'type_examen': c.type_examen.nom,
        }
        for c in CommandeLabo.objects.select_related('patient', 'type_examen').all()
    ]


@router.post('/commandes', response=dict, auth=jwt_auth)
def create_commande(request, payload: CommandeLaboInSchema):
    commande = CommandeLabo(**payload.dict())
    commande.full_clean()
    commande.save()
    log_audit(request, AuditLog.ActionType.CREATE, commande)
    return {'id': commande.id, 'numero_commande': commande.numero_commande, 'statut': commande.statut}


@router.post('/commandes/{commande_id}/resultats', response=dict, auth=jwt_auth)
def saisir_resultat(request, commande_id: int, payload: ResultatLaboInSchema):
    commande = CommandeLabo.objects.get(pk=commande_id)
    resultat, _created = ResultatLabo.objects.get_or_create(
        commande=commande,
        defaults={
            'valeur': payload.valeur,
            'unite': payload.unite,
            'reference': payload.reference,
            'saisi_par': request.user,
        },
    )
    commande.statut = CommandeLabo.Statut.SAISIE
    commande.save(update_fields=['statut', 'updated_at'])
    log_audit(request, AuditLog.ActionType.UPDATE, resultat)
    return {'id': resultat.id, 'valide': resultat.valide}


@router.post('/commandes/{commande_id}/valider', response=dict, auth=jwt_auth)
def valider_resultat(request, commande_id: int):
    commande = CommandeLabo.objects.get(pk=commande_id)
    if not hasattr(commande, 'resultat'):
        raise HttpError(400, 'Aucun résultat à valider')
    old = serialize_for_audit(commande.resultat)
    commande.resultat.valider(request.user)
    log_audit(request, AuditLog.ActionType.VALIDATE, commande.resultat, old_value=old)
    return {'statut': commande.statut, 'valide': True}


@router.post('/commandes/{commande_id}/publier', response=dict, auth=jwt_auth)
def publier_resultat(request, commande_id: int):
    commande = CommandeLabo.objects.get(pk=commande_id)
    if not hasattr(commande, 'resultat') or not commande.resultat.valide:
        raise HttpError(400, 'Le résultat doit être validé avant publication')
    url = save_labo_report_pdf(commande.resultat)
    commande.resultat.publie = True
    commande.resultat.save(update_fields=['publie'])
    commande.statut = CommandeLabo.Statut.PUBLIEE
    commande.save(update_fields=['statut', 'updated_at'])
    log_audit(request, AuditLog.ActionType.PUBLISH, commande.resultat)
    return {'statut': commande.statut, 'rapport_pdf': url}


@router.get('/commandes/{commande_id}/rapport-pdf', auth=jwt_auth)
def download_rapport_pdf(request, commande_id: int):
    from django.http import HttpResponse
    commande = CommandeLabo.objects.select_related('patient', 'type_examen', 'medecin_prescripteur').get(pk=commande_id)
    if not hasattr(commande, 'resultat'):
        raise HttpError(404, 'Aucun résultat disponible')
    pdf_bytes = generate_labo_report_pdf(commande, commande.resultat)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rapport_{commande.numero_commande}.pdf"'
    return response
