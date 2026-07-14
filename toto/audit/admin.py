from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action_type', 'model_name', 'object_id', 'ip_address')
    list_filter = ('action_type', 'model_name')
    search_fields = ('object_id', 'description', 'user__username')
    readonly_fields = (
        'user', 'timestamp', 'ip_address', 'action_type',
        'model_name', 'object_id', 'old_value', 'new_value', 'description',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
