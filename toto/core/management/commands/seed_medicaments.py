from django.core.management.base import BaseCommand

from pharmacie.seed_utils import seed_medicament_catalog


class Command(BaseCommand):
    help = 'Charge le catalogue complet des médicaments (toutes pathologies majeures)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement du catalogue pharmaceutique SGHL...')
        seed_medicament_catalog(self.stdout, self.style)
