# apps/security/models.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.contrib.postgres.fields import JSONField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user with email login and role-based classification.
    """
    class Roles(models.TextChoices):
        ADMIN         = "ADMIN", "Admin"
        DOCTOR        = "DOCTOR", "Doctor"
        NURSE         = "NURSE", "Nurse"
        RECEPTIONIST  = "RECEPTIONIST", "Receptionist"
        PATIENT       = "PATIENT", "Patient"

    email     = models.EmailField(unique=True)
    role      = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
        db_index=True
    )
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


def log_user_action(sender, instance, **kwargs):
    """
    Stub for hooking into model saves/deletes to write AuditLog entries.
    Populate with thread/request-local user, diff, etc.
    """
    pass


class BaseLog(models.Model):
    timestamp   = models.DateTimeField(auto_now_add=True, db_index=True)
    user        = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    user_agent  = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract  = True
        ordering  = ["-timestamp"]


class AuditLog(BaseLog):
    action       = models.CharField(max_length=100, db_index=True)
    content_type = models.ForeignKey(
        "contenttypes.ContentType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id    = models.CharField(max_length=255, blank=True)
    object_repr  = models.CharField(max_length=200, blank=True)
    changes      = JSONField(default=dict, blank=True)

    class Meta:
        db_table             = "security_audit_log"
        verbose_name         = "Audit Log"
        verbose_name_plural  = "Audit Logs"

    def __str__(self):
        return f"{self.timestamp.isoformat()} | {self.user} | {self.action}"


class RequestLog(BaseLog):
    path        = models.CharField(max_length=200)
    method      = models.CharField(max_length=10)
    status_code = models.PositiveSmallIntegerField()
    duration_ms = models.PositiveIntegerField()

    class Meta:
        db_table             = "security_request_log"
        verbose_name         = "Request Log"
        verbose_name_plural  = "Request Logs"

    def __str__(self):
        return f"{self.method} {self.path} [{self.status_code}]"