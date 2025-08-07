# apps/appointments/admin.py

from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "token_number",
        "patient",
        "doctor",
        "appointment_time",
        "status",
    )
    list_filter = ("status", "doctor", "appointment_time")
    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "patient__mrn",
        "doctor__username",
    )
    ordering = ("-appointment_time",)