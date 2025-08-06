from .models import AuditLog
from .signals import get_client_ip


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            AuditLog.objects.create(
                user=user,
                action='request',
                path=request.path,
                method=request.method,
                ip_address=get_client_ip(request)
            )
        return response