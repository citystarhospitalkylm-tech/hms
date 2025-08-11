# apps/patients/models.py

import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def generate_mrn() -> str:
    """Auto-generate a unique MRN (first 10 chars of UUID4)."""
    return uuid.uuid4().hex[:10].upper()


class Patient(models.Model):
    mrn = models.CharField(
        _("Medical Record Number"),
        max_length=10,
        unique=True,
        default=generate_mrn,
        editable=False,
    )
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    dob = models.DateField(_("Date of Birth"))
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    gender = models.CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(_("Blood Group"), max_length=3)
    allergies = models.TextField(_("Allergies"), blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="patients_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="patients_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    

    class Meta:
        app_label = 'patients'
        ordering = ["-created_at"]
        permissions = [
            ("view_patient", "Can view patient"),
            ("add_patient", "Can add patient"),
            ("change_patient", "Can change patient"),
            ("delete_patient", "Can delete patient"),
        ]

    def __str__(self):
        return f"{self.mrn} – {self.first_name} {self.last_name}"