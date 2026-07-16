"""Sert l'application Flutter web sous /mobile/ (fonctionne aussi si DEBUG=False)."""
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.views.decorators.http import require_GET

MOBILE_DIST = Path(settings.BASE_DIR) / 'mobile_dist'

CONTENT_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.wasm': 'application/wasm',
    '.frag': 'text/plain; charset=utf-8',
    '.bin': 'application/octet-stream',
}


def _safe_path(relative: str) -> Path:
    relative = relative.replace('\\', '/').lstrip('/')
    target = (MOBILE_DIST / relative).resolve()
    root = MOBILE_DIST.resolve()
    if not str(target).startswith(str(root)):
        raise Http404('Chemin invalide')
    return target


def _file_response(path: Path) -> FileResponse:
    if not path.is_file():
        raise Http404('Fichier introuvable')
    content_type = CONTENT_TYPES.get(path.suffix.lower(), 'application/octet-stream')
    response = FileResponse(path.open('rb'), content_type=content_type)
    # Cache court pour les assets hashés / build Flutter
    if path.suffix.lower() in {'.js', '.wasm', '.png', '.woff', '.woff2', '.ttf', '.otf'}:
        response['Cache-Control'] = 'public, max-age=3600'
    else:
        response['Cache-Control'] = 'no-cache'
    return response


def _missing_build_page() -> HttpResponse:
    return HttpResponse(
        '<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>SGHL Mobile</title></head>'
        '<body style="font-family:system-ui,sans-serif;padding:2rem;max-width:640px;margin:auto">'
        '<h1>SGHL Mobile — build manquant</h1>'
        '<p>Le dossier <code>mobile_dist/</code> est absent sur le serveur.</p>'
        '<pre style="background:#f1f5f9;padding:1rem;border-radius:12px">'
        'cd toto/mobile\n'
        'flutter build web --release --base-href /mobile/\n'
        '# puis copier build/web vers toto/mobile_dist'
        '</pre></body></html>',
        content_type='text/html; charset=utf-8',
        status=503,
    )


@require_GET
def mobile_index(request):
    index = MOBILE_DIST / 'index.html'
    if not index.is_file():
        return _missing_build_page()
    return _file_response(index)


@require_GET
def mobile_asset(request, path):
    if not path or path.endswith('/'):
        return mobile_index(request)

    try:
        target = _safe_path(path)
        if target.is_file():
            return _file_response(target)
    except Http404:
        pass

    # Fallback SPA Flutter (routes sans extension)
    if '.' not in Path(path).name:
        return mobile_index(request)

    raise Http404(f'Asset mobile introuvable: {path}')
