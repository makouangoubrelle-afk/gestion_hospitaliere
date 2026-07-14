from django.db import models


class SiteLocalise(models.Model):
    class TypeLieu(models.TextChoices):
        HOPITAL = 'hopital', 'Hôpital'
        CLINIQUE = 'clinique', 'Clinique'
        URGENCES = 'urgences', 'Service des urgences'
        LABORATOIRE = 'laboratoire', 'Laboratoire'
        PHARMACIE = 'pharmacie', 'Pharmacie'
        AMBULANCE = 'ambulance', 'Ambulance / Mobile'
        DEPISTAGE = 'depistage', 'Centre de dépistage'

    nom = models.CharField(max_length=150)
    type_lieu = models.CharField(max_length=30, choices=TypeLieu.choices, default=TypeLieu.HOPITAL)
    adresse = models.TextField(blank=True)
    ville = models.CharField(max_length=100, default='Dakar')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    telephone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Site géolocalisé'
        verbose_name_plural = 'Sites géolocalisés'

    def __str__(self):
        return f"{self.nom} — {self.ville}"
