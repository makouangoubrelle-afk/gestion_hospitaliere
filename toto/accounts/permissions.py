from functools import wraps
from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import redirect

from .models import Role


def _redirect_login(request):
    return redirect(f'/login/?next={quote(request.get_full_path())}')


def is_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profile = getattr(user, 'profile', None)
    return profile is not None and profile.role == Role.ADMIN


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return _redirect_login(request)
        if not is_admin(request.user):
            messages.error(request, 'Accès réservé aux administrateurs.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
