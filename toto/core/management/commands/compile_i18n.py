from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Compile les fichiers .po en .mo (compatible Windows)'

    def handle(self, *args, **options):
        try:
            import polib
        except ImportError:
            self.stderr.write(self.style.ERROR('Exécutez : pip install polib'))
            return

        locale_dir = Path(settings.BASE_DIR) / 'locale'
        if not locale_dir.exists():
            self.stderr.write(self.style.WARNING(f'Dossier introuvable : {locale_dir}'))
            return

        count = 0
        for po_path in locale_dir.rglob('*.po'):
            mo_path = po_path.with_suffix('.mo')
            po = polib.pofile(str(po_path))
            po.save_as_mofile(str(mo_path))
            count += 1
            self.stdout.write(self.style.SUCCESS(f'Compilé : {mo_path.name}'))

        self.stdout.write(self.style.SUCCESS(f'{count} langue(s) prête(s).'))
