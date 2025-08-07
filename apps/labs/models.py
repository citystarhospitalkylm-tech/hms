# apps/labs/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class LabTest(models.Model):
    code = models.CharField(_("Test Code"), max_length=50, unique=True)
    name = models.CharField(_("Test Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_("Active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="labtests_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="labtests_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        ordering = ["code"]
        permissions = [
            ("view_labtest", "Can view lab test"),
            ("add_labtest", "Can add lab test"),
            ("change_labtest", "Can change lab test"),
            ("delete_labtest", "Can delete lab test"),
        ]

    def __str__(self):
        return f"{self.code} – {self.name}"


class LabOrder(models.Model):
    class Status(models.TextChoices):
        ORDERED   = "ORDERED", _("Ordered")
        COMPLETED = "COMPLETED", _("Completed")
        CANCELLED = "CANCELLED", _("Cancelled")

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.PROTECT,
        related_name="lab_orders",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="lab_orders",
    )
    test = models.ForeignKey(
        LabTest,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    ordered_at = models.DateTimeField(
        _("Ordered At"), default=timezone.now
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=Status.choices,
        default=Status.ORDERED,
    )
    result = models.TextField(_("Result"), blank=True)
    result_at = models.DateTimeField(
        _("Result At"), null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="laborders_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="laborders_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        ordering = ["-ordered_at"]
        permissions = [
            ("view_laborder", "Can view lab order"),
            ("add_laborder", "Can add lab order"),
            ("change_laborder", "Can change lab order"),
            ("delete_laborder", "Can delete lab order"),
        ]

    def __str__(self):
        return f"Order#{self.id} – {self.patient} / {self.test.name}"