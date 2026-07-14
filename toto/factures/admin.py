from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'issue_date', 'total_amount', 'paid_amount', 'status')
    list_filter = ('status', 'issue_date', 'created_at')
    search_fields = ('invoice_number', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('invoice_number', 'patient', 'consultation', 'issue_date', 'due_date')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax', 'total_amount', 'paid_amount')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Additional Information', {
            'fields': ('description', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

