from django.contrib import admin
from .models import Medecin


@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'license_number', 'specialty', 'department', 'status')
    list_filter = ('status', 'specialty', 'created_at')
    search_fields = ('first_name', 'last_name', 'license_number', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('license_number', 'specialty', 'department', 'years_experience')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

