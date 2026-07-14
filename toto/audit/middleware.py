from django.utils.deprecation import MiddlewareMixin

from audit.utils import get_client_ip
from .models import AuditLog


class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._audit_ip = get_client_ip(request)
