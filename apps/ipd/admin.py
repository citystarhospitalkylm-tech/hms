from django.contrib import admin
from .models import Ward, Bed, Admission, Discharge, VitalSign

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('ward', 'bed_number', 'is_occupied')
    list_filter = ('ward','is_occupied')

class VitalSignInline(admin.TabularInline):
    model = VitalSign
    extra = 0
    readonly_fields = ('recorded_at','recorded_by')

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'ward', 'bed', 'status', 'admitted_at')
    list_filter = ('ward','status')
    inlines = [VitalSignInline]

@admin.register(Discharge)
class DischargeAdmin(admin.ModelAdmin):
    list_display = ('admission', 'discharged_by', 'discharged_at')