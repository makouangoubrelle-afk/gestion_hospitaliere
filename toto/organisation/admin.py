from django.contrib import admin

from .models import FileAttente, SalleAttente, SalleUrgence


@admin.register(SalleUrgence)
class SalleUrgenceAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'statut', 'capacite', 'patient', 'medecin')


@admin.register(SalleAttente)
class SalleAttenteAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'zone', 'capacite', 'is_active')


@admin.register(FileAttente)
class FileAttenteAdmin(admin.ModelAdmin):
    list_display = ('patient', 'salle_attente', 'priorite', 'statut', 'heure_arrivee')
    list_filter = ('statut', 'priorite')
