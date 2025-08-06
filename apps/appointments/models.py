import uuid
from datetime import date
from django.db import models, transaction
from django.utils import timezone
from apps.patients.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'PENDING',   'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELED  = 'CANCELED',  'Canceled'
        MISSED    = 'MISSED',    'Missed'

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient         = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor          = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role': User.Roles.DOCTOR})
    scheduled_date  = models.DateField()
    scheduled_time  = models.TimeField()
    is_walkin       = models.BooleanField(default=False)
    token           = models.PositiveIntegerField(editable=False)
    status          = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('scheduled_date', 'token'),)
        ordering = ['scheduled_date', 'token']

    def save(self, *args, **kwargs):
        # For walk-ins: default to today/time
        if self.is_walkin and not self.scheduled_date:
            self.scheduled_date = date.today()
        if self.is_walkin and not self.scheduled_time:
            self.scheduled_time = timezone.now().time()

        # Generate queue token per day
        if not self.token:
            with transaction.atomic():
                last = (
                    Appointment.objects
                    .select_for_update()
                    .filter(scheduled_date=self.scheduled_date)
                    .order_by('token')
                    .last()
                )
                self.token = last.token + 1 if last else 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.scheduled_date} [{self.token}] – {self.patient.patient_id}"