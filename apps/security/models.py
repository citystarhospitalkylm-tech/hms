from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


class BaseLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True
        ordering = ["-timestamp"]


class AuditLog(BaseLog):
    action = models.CharField(max_length=100, db_index=True)
    content_type = models.ForeignKey(
        "contenttypes.ContentType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    object_id = models.CharField(max_length=255, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)
    changes = JSONField(default=dict, blank=True)

    class Meta:
        db_table = "security_audit_log"
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"{self.timestamp.isoformat()} | {self.user} | {self.action}"


class RequestLog(BaseLog):
    path = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.PositiveSmallIntegerField()
    duration_ms = models.PositiveIntegerField()

    class Meta:
        db_table = "security_request_log"
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"{self.method} {self.path} [{self.status_code}]"