import logging

from django.db import transaction
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from .models import AuditLog
from .utils import get_client_ip

logger = logging.getLogger("security.signals")


def _create_audit_log(user, action, instance=None, changes=None, request=None):
    """
    Helper to write an AuditLog entry safely after the DB transaction commits.
    """
    def _log():
        AuditLog.objects.create(
            user=user,
            action=action,
            content_type=ContentType.objects.get_for_model(instance) if instance else None,
            object_id=str(getattr(instance, "pk", "")) if instance else "",
            object_repr=repr(instance)[:200] if instance else "",
            changes=changes or {},
            ip_address=get_client_ip(request) if request else None,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:255] if request else "",
        )

    try:
        transaction.on_commit(_log)
    except Exception as exc:
        logger.exception("AuditLog failed: %s", exc)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    _create_audit_log(user, "user_login", request=request)


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    _create_audit_log(user, "user_logout", request=request)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    _create_audit_log(None, "user_login_failed", changes={"credentials": credentials}, request=request)


@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    # skip logging for the log models themselves
    if instance.__class__.__module__.startswith("security.models"):
        return

    action = "created" if created else "updated"
    _create_audit_log(
        instance._meta.model_name,
        f"{sender._meta.label_lower}.{action}",
        instance=instance,
        changes={"fields": getattr(instance, "_dirty_fields", {})},
        request=getattr(instance, "_last_request", None),
    )


@receiver(pre_delete)
def log_model_delete(sender, instance, **kwargs):
    if instance.__class__.__module__.startswith("security.models"):
        return

    _create_audit_log(
        instance._meta.model_name,
        f"{sender._meta.label_lower}.deleted",
        instance=instance,
        request=getattr(instance, "_last_request", None),
    )