from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display    = ('patient_id', 'first_name', 'last_name', 'dob', 'gender', 'phone')
    search_fields   = ('patient_id', 'first_name', 'last_name', 'phone')
    list_filter     = ('gender',)
    readonly_fields = ('id', 'patient_id', 'qr_code', 'created_at', 'updated_at')