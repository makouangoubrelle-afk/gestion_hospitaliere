from django.contrib import admin

from .models import CommandeLabo, Prelevement, ResultatLabo, TypeExamen


@admin.register(TypeExamen)
class TypeExamenAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'prix', 'is_active')


@admin.register(CommandeLabo)
class CommandeLaboAdmin(admin.ModelAdmin):
    list_display = ('numero_commande', 'patient', 'type_examen', 'statut', 'created_at')
    list_filter = ('statut',)


@admin.register(Prelevement)
class PrelevementAdmin(admin.ModelAdmin):
    list_display = ('echantillon_id', 'commande', 'date_prelevement')


@admin.register(ResultatLabo)
class ResultatLaboAdmin(admin.ModelAdmin):
    list_display = ('commande', 'valide', 'publie', 'date_validation')
    list_filter = ('valide', 'publie')
