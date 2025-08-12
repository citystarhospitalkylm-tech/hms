from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'appointment_time', 'status']
    list_filter = ['status', 'doctor']
    search_fields = ['patient__name', 'doctor__name']