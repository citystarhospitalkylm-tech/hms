from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display    = ('scheduled_date', 'token', 'patient', 'doctor', 'status', 'is_walkin')
    list_filter     = ('scheduled_date', 'status', 'is_walkin', 'doctor')
    search_fields   = ('patient__patient_id', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('id', 'token', 'created_at', 'updated_at')