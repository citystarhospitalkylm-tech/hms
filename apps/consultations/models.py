# apps/consultations/models.py

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # e.g. "security.User"

class Consultation(models.Model):
    patient      = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="consultations_as_patient"
    )
    doctor       = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="consultations_as_doctor"
    )
    scheduled_at = models.DateTimeField(db_index=True)
    notes        = models.TextField(blank=True)

    class Meta:
        db_table            = "consultations_consultation"
        ordering            = ["-scheduled_at"]
        verbose_name        = "Consultation"
        verbose_name_plural = "Consultations"

    def __str__(self):
        return f"{self.scheduled_at:%Y-%m-%d %H:%M} | Dr. {self.doctor}"


class Prescription(models.Model):
    consultation  = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    patient       = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="prescriptions_for_patient"
    )
    prescribed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="prescriptions_created"
    )
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = "consultations_prescription"
        ordering            = ["-created_at"]
        verbose_name        = "Prescription"
        verbose_name_plural = "Prescriptions"

    def __str__(self):
        return f"Rx #{self.id} for {self.patient}"


class PrescriptionItem(models.Model):
    prescription  = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items"
    )
    medication    = models.CharField(max_length=255)
    dosage        = models.CharField(max_length=100)
    instructions  = models.TextField(blank=True)

    class Meta:
        db_table            = "consultations_prescription_item"
        verbose_name        = "Prescription Item"
        verbose_name_plural = "Prescription Items"

    def __str__(self):
        return f"{self.medication} ({self.dosage})"