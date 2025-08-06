from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display     = ('invoice_number', 'patient', 'status', 'total_amount', 'paid_amount', 'outstanding_amount', 'due_date')
    readonly_fields  = ('sequence', 'invoice_number', 'created_by', 'created_at', 'status')
    list_filter      = ('status',)
    search_fields    = ('invoice_number', 'patient__patient_id')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display    = ('invoice', 'description', 'amount')
    search_fields   = ('description',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display    = ('invoice', 'amount', 'method', 'paid_at', 'processed_by')
    list_filter     = ('method',)
    readonly_fields = ('paid_at', 'processed_by')