from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.timezone import now
from .models import AuditLog


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='login',
        path=request.path,
        method='POST',
        ip_address=get_client_ip(request)
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='logout',
        path=request.path,
        method='POST',
        ip_address=get_client_ip(request)
    )