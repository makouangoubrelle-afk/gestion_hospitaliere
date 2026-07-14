from django.contrib import admin

from .models import PlanningGarde, RendezVous


@admin.register(PlanningGarde)
class PlanningGardeAdmin(admin.ModelAdmin):
    list_display = ('medecin', 'date_debut', 'date_fin', 'service')


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_rdv', 'statut')
    list_filter = ('statut',)
