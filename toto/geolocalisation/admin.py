from django.contrib import admin

from .models import SiteLocalise


@admin.register(SiteLocalise)
class SiteLocaliseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_lieu', 'ville', 'latitude', 'longitude', 'is_active')
    list_filter = ('type_lieu', 'ville', 'is_active')
    search_fields = ('nom', 'adresse', 'ville')
