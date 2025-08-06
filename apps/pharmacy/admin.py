from django.contrib import admin
from .models import Medicine, Batch, PharmacySale, SaleItem


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display    = ('name', 'unit_price', 'total_stock', 'low_stock_threshold')
    search_fields   = ('name',)
    readonly_fields = ('total_stock',)


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display  = ('medicine', 'batch_number', 'expiry_date', 'quantity')
    list_filter   = ('medicine', 'expiry_date')
    search_fields = ('batch_number',)


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('unit_price', 'total_price')


@admin.register(PharmacySale)
class PharmacySaleAdmin(admin.ModelAdmin):
    list_display    = ('id', 'patient', 'sale_date', 'sold_by', 'total_amount')
    inlines         = [SaleItemInline]
    readonly_fields = ('sale_date', 'total_amount')
    search_fields   = ('patient__patient_id',)