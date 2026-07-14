from django.contrib import admin

from .models import (
    Batiment, Chambre, ConstanteVitale, Hospitalisation,
    Lit, ServiceHospitalier, TransfertService,
)


@admin.register(Batiment)
class BatimentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'is_active')


@admin.register(ServiceHospitalier)
class ServiceHospitalierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'batiment', 'is_active')
    list_filter = ('batiment',)


@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'service', 'etage', 'capacite')


@admin.register(Lit)
class LitAdmin(admin.ModelAdmin):
    list_display = ('numero', 'chambre', 'statut', 'patient_actuel')
    list_filter = ('statut',)


@admin.register(Hospitalisation)
class HospitalisationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'lit', 'medecin_referent', 'date_entree', 'date_sortie_prevue', 'statut')
    list_filter = ('statut',)


admin.site.register(TransfertService)
admin.site.register(ConstanteVitale)
