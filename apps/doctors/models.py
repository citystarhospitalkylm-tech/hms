# apps/doctors/models.py

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Doctor(models.Model):
    class Status(models.TextChoices):
        ACTIVE    = "ACTIVE", _("Active")
        INACTIVE  = "INACTIVE", _("Inactive")
        SUSPENDED = "SUSPENDED", _("Suspended")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )
    specialty = models.CharField(_("Specialty"), max_length=100)
    qualifications = models.TextField(_("Qualifications"), blank=True)
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    department = models.CharField(_("Department"), max_length=100, blank=True)
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

   

created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    editable=False,
    related_name="created_%(class)s_set",
)

updated_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    editable=False,
    related_name="updated_%(class)s_set",
)   
class Meta:
        ordering = ["user__last_name", "user__first_name"]
        #permissions = [
         #   ("view_doctor", "Can view doctor"),
          #  ("add_doctor", "Can add doctor"),
           # ("change_doctor", "Can change doctor"),
            #("delete_doctor", "Can delete doctor"),
       # ]

        def __str__(self):
          return f"Dr. {self.user.get_full_name()} – {self.specialty}"

        def save(self, *args, **kwargs):
        # Ensure created_by / updated_by are set from context if passed
          super().save(*args, **kwargs)