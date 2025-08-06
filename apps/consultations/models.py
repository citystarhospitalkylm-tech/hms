import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.patients.models import Patient

User = get_user_model()

class Consultation(models.Model):
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient        = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='consultations')
    doctor         = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role': User.Roles.DOCTOR})
    date           = models.DateField(default=timezone.now)
    time           = models.TimeField(default=timezone.now)
    symptoms       = models.TextField()
    diagnosis      = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.date} {self.patient.patient_id} by {self.doctor.email}"

class Prescription(models.Model):
    consultation = models.OneToOneField(
        Consultation, on_delete=models.CASCADE, related_name='prescription'
    )
    created_at   = models.DateTimeField(auto_now_add=True)
    created_by   = models.ForeignKey(User, on_delete=models.PROTECT)
    notes        = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.consultation}"

class PrescriptionItem(models.Model):
    prescription  = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name='items'
    )
    medicine_name = models.CharField(max_length=200)
    dosage        = models.CharField(max_length=100)
    frequency     = models.CharField(max_length=100)
    duration      = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicine_name} for {self.prescription}"

class Referral(models.Model):
    MODULE_CHOICES = (
        ('LAB',       'Laboratory'),
        ('RADIOLOGY', 'Radiology'),
        ('OTHER',     'Other'),
    )
    consultation = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name='referrals'
    )
    module       = models.CharField(max_length=10, choices=MODULE_CHOICES)
    details      = models.TextField(blank=True)
    referred_by  = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.module} referral for {self.consultation}"