from django.contrib import admin
from .models import Supplier, DrugCategory, Drug, Batch, SaleItem

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display  = ('name', 'contact_email', 'created_at')
    search_fields = ('name',)

@admin.register(DrugCategory)
class DrugCategoryAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'unit_price', 'created_at')
    list_filter   = ('category',)
    search_fields = ('name',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display  = ('batch_no', 'drug', 'quantity', 'expiry_date')
    list_filter   = ('expiry_date',)
    search_fields = ('batch_no',)

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display  = ('batch', 'quantity_sold', 'sold_at', 'unit_price')
    list_filter   = ('sold_at',)