# apps/patients/admin.py

from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "mrn",
        "first_name",
        "last_name",
        "dob",
        "gender",
        "phone_number",
        "created_at",
    )
    search_fields = ("mrn", "first_name", "last_name", "phone_number")
    list_filter = ("gender", "blood_group")