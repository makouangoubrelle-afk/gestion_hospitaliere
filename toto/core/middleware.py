from urllib.parse import quote

from django.shortcuts import redirect
from django.urls import reverse

from core.redirects import resolve_legacy_redirect


class LoginRequiredMiddleware:
    """Redirige vers /login/ si non connecté ; gère les anciennes URL."""

    EXEMPT_PREFIXES = (
        '/login',
        '/register',
        '/logout',
        '/i18n/',
        '/static/',
        '/api/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        legacy_name = resolve_legacy_redirect(path)
        if legacy_name:
            target = reverse(legacy_name)
            if request.GET:
                target = f'{target}?{request.GET.urlencode()}'
            return redirect(target)

        if not request.user.is_authenticated:
            if not any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
                target = path
                if request.GET:
                    target = f'{path}?{request.GET.urlencode()}'
                return redirect(f'/login/?next={quote(target)}')

        return self.get_response(request)
