# apps/doctors/admin.py

from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "specialty",
        "department",
        "phone",
        "status",
    )
    list_filter = ("status", "department", "specialty")
    search_fields = (
        "user__first_name",
        "user__last_name",
        "specialty",
        "department",
    )
    ordering = ("user__last_name",)