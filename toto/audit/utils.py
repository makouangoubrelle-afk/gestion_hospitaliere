import json

from django.forms.models import model_to_dict

from .models import AuditLog


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def log_audit(request, action_type, instance, old_value=None, description=''):
    new_value = None
    if instance is not None:
        try:
            new_value = serialize_for_audit(instance)
        except Exception:
            new_value = {'id': str(getattr(instance, 'pk', ''))}

    AuditLog.objects.create(
        user=request.user if getattr(request, 'user', None) and request.user.is_authenticated else (
            instance if getattr(instance, 'is_authenticated', False) else None
        ),
        ip_address=get_client_ip(request) if request else None,
        action_type=action_type,
        model_name=instance.__class__.__name__ if instance else 'System',
        object_id=str(getattr(instance, 'pk', '')),
        old_value=old_value,
        new_value=new_value,
        description=description,
    )


def serialize_for_audit(instance):
    if instance is None:
        return None
    data = model_to_dict(instance)
    for key, value in list(data.items()):
        if hasattr(value, 'isoformat'):
            data[key] = value.isoformat()
    return data
