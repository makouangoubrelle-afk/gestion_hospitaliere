from django.contrib import admin

from .models import LotMedicament, Medicament, MouvementStock, Prescription


@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'seuil_alerte', 'is_active')


@admin.register(LotMedicament)
class LotMedicamentAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'numero_lot', 'quantite', 'date_peremption')


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('lot', 'type_mouvement', 'quantite', 'created_at')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'medicament', 'statut', 'quantite', 'validee_at')
    list_filter = ('statut',)
