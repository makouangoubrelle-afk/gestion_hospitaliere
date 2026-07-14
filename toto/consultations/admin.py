from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'appointment_date', 'visit_type', 'status')
    list_filter = ('status', 'visit_type', 'appointment_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'medecin__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Consultation Details', {
            'fields': ('patient', 'medecin', 'visit_type', 'appointment_date', 'completed_date', 'duration_minutes')
        }),
        ('Medical Information', {
            'fields': ('chief_complaint', 'diagnosis', 'treatment_plan', 'notes')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

