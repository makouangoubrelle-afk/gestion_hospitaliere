from django.contrib import admin

from .models import Infirmier


@admin.register(Infirmier)
class InfirmierAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'matricule', 'service', 'grade', 'unite', 'status')
    list_filter = ('status', 'service', 'grade')
    search_fields = ('first_name', 'last_name', 'matricule', 'email')
