from django.contrib import admin
from .models import (
    Ward, Room, Bed, Admission, VitalSign,
    NursingNote, Round, ServiceUsage, DischargeSummary
)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display    = ('ward', 'number', 'capacity')
    list_filter     = ('ward',)


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display    = ('room', 'number', 'is_available')
    list_filter     = ('room__ward', 'is_available')


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display    = ('patient', 'bed', 'status', 'admitted_at', 'discharged_at')
    list_filter     = ('status', 'ward')


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display    = ('admission', 'recorded_at', 'temperature', 'pulse', 'respiration')


@admin.register(NursingNote)
class NursingNoteAdmin(admin.ModelAdmin):
    list_display    = ('admission', 'created_at', 'created_by')


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display    = ('admission', 'doctor', 'at_time')


@admin.register(ServiceUsage)
class ServiceUsageAdmin(admin.ModelAdmin):
    list_display    = ('admission', 'service', 'quantity', 'created_at')


@admin.register(DischargeSummary)
class DischargeSummaryAdmin(admin.ModelAdmin):
    list_display    = ('admission', 'created_at', 'created_by')