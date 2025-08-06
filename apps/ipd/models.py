import uuid
from django.db import models, transaction
from django.utils import timezone
from apps.patients.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()


class Ward(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    ward        = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='rooms')
    number      = models.CharField(max_length=10)
    capacity    = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('ward', 'number')

    def __str__(self):
        return f"{self.ward.name} - Room {self.number}"


class Bed(models.Model):
    room         = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    number       = models.CharField(max_length=5)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('room', 'number')

    def __str__(self):
        status = 'Available' if self.is_available else 'Occupied'
        return f"{self.room} | Bed {self.number} ({status})"


class Admission(models.Model):
    class Status(models.TextChoices):
        ADMITTED   = 'ADMITTED',  'Admitted'
        DISCHARGED = 'DISCHARGED','Discharged'

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient         = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='admissions')
    ward            = models.ForeignKey(Ward, on_delete=models.PROTECT)
    room            = models.ForeignKey(Room, on_delete=models.PROTECT)
    bed             = models.ForeignKey(Bed, on_delete=models.PROTECT)
    admitted_by     = models.ForeignKey(User, on_delete=models.PROTECT, related_name='admitted_patients')
    admitted_at     = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(max_length=10, choices=Status.choices, default=Status.ADMITTED)
    discharged_at   = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (('bed', 'status'),)

    def save(self, *args, **kwargs):
        # On first save, mark bed occupied
        if not self.pk:
            with transaction.atomic():
                bed = Bed.objects.select_for_update().get(pk=self.bed.pk)
                if not bed.is_available:
                    raise ValueError("Bed is already occupied")
                bed.is_available = False
                bed.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.patient_id} in {self.bed}"


class VitalSign(models.Model):
    admission   = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='vitals')
    recorded_at = models.DateTimeField(default=timezone.now)
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    pulse       = models.PositiveIntegerField()
    respiration = models.PositiveIntegerField()
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"Vitals of {self.admission} at {self.recorded_at}"


class NursingNote(models.Model):
    admission   = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='nursing_notes')
    note        = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Note for {self.admission} at {self.created_at}"


class Round(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='rounds')
    doctor    = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role': User.Roles.DOCTOR})
    at_time   = models.DateTimeField(default=timezone.now)
    notes     = models.TextField()

    def __str__(self):
        return f"Round by {self.doctor.email} at {self.at_time}"


class ServiceUsage(models.Model):
    SERVICE_CHOICES = (
        ('OXYGEN', 'Oxygen'),
        ('NURSING', 'Nursing Care'),
        ('OTHER',   'Other'),
    )
    admission   = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='services')
    service     = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    details     = models.TextField(blank=True)
    quantity    = models.PositiveIntegerField(default=1)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service} x{self.quantity} for {self.admission}"


class DischargeSummary(models.Model):
    admission      = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='discharge_summary')
    summary        = models.TextField()
    created_by     = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at     = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Mark discharge time, free the bed
            adm = self.admission
            if adm.status == Admission.Status.DISCHARGED:
                super().save(*args, **kwargs)
                return
            adm.status = Admission.Status.DISCHARGED
            adm.discharged_at = timezone.now()
            adm.save()
            bed = Bed.objects.select_for_update().get(pk=adm.bed.pk)
            bed.is_available = True
            bed.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Discharge Summary for {self.admission}"