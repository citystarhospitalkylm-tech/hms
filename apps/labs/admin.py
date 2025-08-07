# apps/labs/admin.py

from django.contrib import admin
from .models import LabTest, LabOrder


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "test",
        "doctor",
        "ordered_at",
        "status",
    )
    list_filter = ("status", "test", "ordered_at")
    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "test__name",
    )
    ordering = ("-ordered_at",)