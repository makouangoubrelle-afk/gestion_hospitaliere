from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'full_name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'patient_id', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'postal_code', 'country')
        }),
        ('Medical Information', {
            'fields': ('patient_id', 'blood_type', 'allergies', 'medical_history')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

