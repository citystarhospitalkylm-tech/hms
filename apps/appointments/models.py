# apps/appointments/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Appointment(models.Model):
    class Status(models.TextChoices):
        BOOKED   = "BOOKED", _("Booked")
        CANCELLED = "CANCELLED", _("Cancelled")
        VISITED  = "VISITED", _("Visited")
        NO_SHOW  = "NO_SHOW", _("No-show")

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="doctor_appointments",
    )
    appointment_time = models.DateTimeField(_("Appointment Time"))
    token_number = models.PositiveIntegerField(
        _("Token Number"),
        editable=False,
        null=True,
        blank=True,
        help_text="Auto-generated per doctor per day",
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=Status.choices,
        default=Status.BOOKED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="appointments_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="appointments_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        ordering = ["appointment_time"]
        unique_together = [
            ("doctor", "appointment_time")
        ]  # prevent double-book
        permissions = [
            ("view_appointment", "Can view appointment"),
            ("add_appointment", "Can add appointment"),
            ("change_appointment", "Can change appointment"),
            ("delete_appointment", "Can delete appointment"),
        ]

    def save(self, *args, **kwargs):
        # Auto-assign token_number on create
        if self._state.adding and self.token_number is None:
            today = timezone.localdate()
            count = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_time__date=today
            ).count()
            self.token_number = count + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.token_number} | {self.patient} @ {self.appointment_time}"