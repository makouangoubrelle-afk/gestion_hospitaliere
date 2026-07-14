from datetime import timedelta

from django.utils import timezone

from .catalog import MEDICAMENT_CATALOG
from .models import LotMedicament, Medicament


def seed_medicament_catalog(stdout=None, style=None):
    """Charge ou met à jour le catalogue pharmaceutique complet."""
    created_count = 0
    updated_count = 0
    lot_count = 0

    for code, nom, forme, dosage, indication, stock, seuil in MEDICAMENT_CATALOG:
        nom_complet = f'{nom} — {indication}'
        medicament, created = Medicament.objects.update_or_create(
            code=code,
            defaults={
                'nom': nom_complet,
                'forme': forme,
                'dosage': dosage,
                'seuil_alerte': seuil,
                'is_active': True,
            },
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

        lot, lot_created = LotMedicament.objects.get_or_create(
            medicament=medicament,
            numero_lot=f'LOT-{code}-001',
            defaults={
                'quantite': stock,
                'date_peremption': timezone.now().date() + timedelta(days=730),
            },
        )
        if lot_created:
            lot_count += 1
        elif lot.quantite < seuil:
            lot.quantite = stock
            lot.save(update_fields=['quantite'])

    total = len(MEDICAMENT_CATALOG)
    if stdout:
        stdout.write(
            f'Catalogue : {total} médicaments '
            f'({created_count} créés, {updated_count} mis à jour, {lot_count} lots ajoutés).'
        )
    if style:
        stdout.write(style.SUCCESS(f'{total} médicaments chargés dans la pharmacie.'))

    return total
