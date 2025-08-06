import uuid
from io import BytesIO

from django.db import models
from django.utils import timezone
from django.core.files import File

import qrcode


class Patient(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    id                        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id                = models.CharField(max_length=10, unique=True, editable=False)
    first_name                = models.CharField(max_length=50)
    last_name                 = models.CharField(max_length=50)
    dob                       = models.DateField()
    gender                    = models.CharField(max_length=1, choices=GENDERS)
    phone                     = models.CharField(max_length=15)
    email                     = models.EmailField(blank=True)
    address                   = models.TextField(blank=True)
    emergency_contact_name    = models.CharField(max_length=100, blank=True)
    emergency_contact_phone   = models.CharField(max_length=15, blank=True)
    insurance_provider        = models.CharField(max_length=100, blank=True)
    insurance_number          = models.CharField(max_length=50, blank=True)
    qr_code                   = models.ImageField(upload_to='patient_qrcodes/', blank=True, null=True)
    created_at                = models.DateTimeField(auto_now_add=True)
    updated_at                = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Sequential patient_id: P000001, P000002, …
            last = Patient.objects.order_by('created_at').last()
            num  = int(last.patient_id.lstrip('P')) + 1 if last else 1
            self.patient_id = f'P{num:06d}'
        super().save(*args, **kwargs)

        if not self.qr_code:
            qr      = qrcode.make(self.patient_id)
            canvas  = BytesIO()
            qr.save(canvas, format='PNG')
            self.qr_code.save(f'{self.patient_id}.png', File(canvas), save=False)
            super().save(update_fields=['qr_code'])