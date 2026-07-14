from django.contrib import admin

from .models import Secretaire


@admin.register(Secretaire)
class SecretaireAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'matricule', 'bureau', 'service_accueil', 'status')
    search_fields = ('first_name', 'last_name', 'matricule', 'email')
