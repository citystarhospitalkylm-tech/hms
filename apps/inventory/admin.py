from django.contrib import admin
from .models import InventoryRecord

@admin.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display  = ('batch', 'current_quantity', 'updated_at')
    list_filter   = ('updated_at',)
    search_fields = ('batch__batch_no', 'batch__drug__name')