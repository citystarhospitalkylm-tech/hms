from django.db import models
from django.conf import settings

class Ward(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Bed(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)

    class Meta:
        unique_together = ('ward', 'bed_number')

    def __str__(self):
        status = 'Occupied' if self.is_occupied else 'Free'
        return f"{self.ward.name}–{self.bed_number} ({status})"

class Admission(models.Model):
    STATUS_CHOICES = [
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    admitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='admissions_made')
    admitted_at = models.DateTimeField(auto_now_add=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='admitted')

    def __str__(self):
        return f"Admission #{self.id} – {self.patient}"

class Discharge(models.Model):
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='discharge')
    discharged_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='discharges_made')
    discharged_at = models.DateTimeField(auto_now_add=True)
    summary_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Discharge for Admission #{self.admission.id}"

class VitalSign(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='vitals')
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    recorded_at = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1)  # °C
    bp_systolic = models.PositiveIntegerField()
    bp_diastolic = models.PositiveIntegerField()
    heart_rate = models.PositiveIntegerField()
    respiratory_rate = models.PositiveIntegerField()

    def __str__(self):
        return f"VS @ {self.recorded_at.strftime('%H:%M')} for Adm#{self.admission.id}"