from django.contrib import admin

from .models import LoginJournal, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'mfa_enabled')
    list_filter = ('role', 'mfa_enabled')
    search_fields = ('user__username', 'user__email')


@admin.register(LoginJournal)
class LoginJournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'success', 'timestamp')
    list_filter = ('success',)
    readonly_fields = ('user', 'ip_address', 'user_agent', 'success', 'timestamp')
