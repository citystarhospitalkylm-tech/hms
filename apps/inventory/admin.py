from django.contrib import admin
from .models import StockChange

@admin.register(StockChange)
class StockChangeAdmin(admin.ModelAdmin):
    list_display    = ('timestamp', 'user', 'medicine', 'batch', 'delta')
    list_filter     = ('medicine', 'user')
    search_fields   = ('medicine__name', 'batch__batch_number', 'note')
    date_hierarchy  = 'timestamp'