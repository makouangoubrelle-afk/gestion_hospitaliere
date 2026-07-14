from pathlib import Path
import os
import sys

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        self._compile_translations()
        self._ensure_database_tables()

    def _ensure_database_tables(self):
        if 'runserver' not in sys.argv:
            return
        skip = {'migrate', 'makemigrations'}
        if skip.intersection(sys.argv):
            return
        try:
            from django.core.management import call_command
            call_command('migrate', '--noinput', verbosity=0)
        except Exception:
            pass

    def _compile_translations(self):
        try:
            import polib
        except ImportError:
            return

        locale_dir = Path(settings.BASE_DIR) / 'locale'
        if not locale_dir.exists():
            return

        for po_path in locale_dir.rglob('*.po'):
            mo_path = po_path.with_suffix('.mo')
            try:
                if mo_path.exists() and mo_path.stat().st_mtime >= po_path.stat().st_mtime:
                    continue
                po = polib.pofile(str(po_path))
                po.save_as_mofile(str(mo_path))
            except Exception:
                continue
