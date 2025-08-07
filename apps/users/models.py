# apps/users/models.py

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user extending Django’s AbstractUser.
    Adds a 'role' field backed by a TextChoices enum.
    """

    class Roles(models.TextChoices):
        ADMIN   = "ADMIN",   "Administrator"
        DOCTOR  = "DOCTOR",  "Doctor"
        NURSE   = "NURSE",   "Nurse"
        PATIENT = "PATIENT", "Patient"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
        db_index=True,
        help_text="Designates the user’s role in the system",
    )


class AuditLog(models.Model):
    """
    Tracks high‐level user actions for audit purposes.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"{self.user.username} – {self.action} @ {self.timestamp}"