from django.contrib import admin
from .models import (
    Consultation, Prescription, PrescriptionItem, Referral
)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display    = ('date','time','patient','doctor')
    list_filter     = ('date','doctor')
    search_fields   = ('patient__patient_id','patient__first_name','patient__last_name')
    readonly_fields = ('id','created_at','updated_at')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display    = ('consultation','created_at','created_by')
    readonly_fields = ('id','created_at')

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display  = ('medicine_name','dosage','frequency','duration')
    search_fields = ('medicine_name',)

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display  = ('consultation','module','referred_by','created_at')
    list_filter   = ('module',)