from django.contrib import admin

from .models import Payment, PaymentMethod


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'invoice', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('payment_method', 'status')
    search_fields = ('transaction_id', 'invoice__invoice_number', 'phone_number')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('gateway', 'is_active', 'updated_at')
