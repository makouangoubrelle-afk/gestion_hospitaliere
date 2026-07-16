"""Sert l'application Flutter web sous /mobile/."""
from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.static import serve


MOBILE_DIST = Path(settings.BASE_DIR) / 'mobile_dist'


def _mobile_file(path: str):
    target = (MOBILE_DIST / path).resolve()
    if not str(target).startswith(str(MOBILE_DIST.resolve())):
        raise Http404('Chemin invalide')
    if not target.is_file():
        raise Http404('Fichier mobile introuvable')
    return target


def mobile_index(request):
    """Page d'entrée Flutter web."""
    index = MOBILE_DIST / 'index.html'
    if not index.is_file():
        return HttpResponse(
            '<!DOCTYPE html><html><body style="font-family:sans-serif;padding:2rem">'
            '<h1>SGHL Mobile</h1>'
            '<p>Build Flutter manquant. Exécutez :</p>'
            '<pre>cd toto/mobile\n'
            'flutter build web --release --base-href /mobile/ --output ../mobile_dist</pre>'
            '</body></html>',
            content_type='text/html',
            status=503,
        )
    return serve(request, 'index.html', document_root=str(MOBILE_DIST))


def mobile_asset(request, path):
    """Assets Flutter (js, css, fonts, icons…)."""
    if not path or path.endswith('/'):
        return mobile_index(request)
    try:
        _mobile_file(path)
    except Http404:
        # SPA fallback → index.html pour les routes Flutter
        if '.' not in Path(path).name:
            return mobile_index(request)
        raise
    return serve(request, path, document_root=str(MOBILE_DIST))
