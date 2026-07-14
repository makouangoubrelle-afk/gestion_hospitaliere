from accounts.permissions import is_admin


def user_permissions(request):
    return {
        'is_admin_user': is_admin(request.user) if request.user.is_authenticated else False,
    }
