# apps/consultations/admin.py

from django.contrib import admin
from .models import Consultation, Prescription, PrescriptionItem

class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display   = ('scheduled_at', 'doctor', 'patient')
    search_fields  = ('doctor__email', 'patient__email')
    list_filter    = ('scheduled_at',)
    date_hierarchy = 'scheduled_at'

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display   = ('id', 'patient', 'prescribed_by', 'created_at')
    inlines        = [PrescriptionItemInline]
    search_fields  = ('patient__email', 'prescribed_by__email')
    list_filter    = ('created_at',)
    date_hierarchy = 'created_at'