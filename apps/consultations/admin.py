from django.contrib import admin
from .models import Prescription, PrescriptionItem #Dispense

class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display  = ('id', 'patient', 'prescribed_by', 'created_at')
    inlines       = [PrescriptionItemInline]
    search_fields = ('patient__username', 'prescribed_by__username')

#@admin.register(Dispense)
#class DispenseAdmin(admin.ModelAdmin):
 #   list_display  = ('prescription_item', 'dispensed_by', 'dispensed_at')
  #  list_filter   = ('dispensed_at',)
   # search_fields = ('prescription_item__id',)