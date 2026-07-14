from django.db import models

from medecins.models import Medecin
from patients.models import Patient


class SalleUrgence(models.Model):
    class Statut(models.TextChoices):
        LIBRE = 'libre', 'Libre'
        OCCUPEE = 'occupee', 'Occupée'
        MAINTENANCE = 'maintenance', 'Maintenance'

    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=120)
    capacite = models.PositiveIntegerField(default=4)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.LIBRE)
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='salles_urgence',
    )
    medecin = models.ForeignKey(
        Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='salles_urgence',
    )
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name = "Salle d'urgence"
        verbose_name_plural = "Salles d'urgence"

    def __str__(self):
        return f"{self.code} — {self.nom}"


class SalleAttente(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=120)
    capacite = models.PositiveIntegerField(default=25)
    zone = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']
        verbose_name = "Salle d'attente"
        verbose_name_plural = "Salles d'attente"

    def __str__(self):
        return f"{self.code} — {self.nom}"

    @property
    def patients_en_attente(self):
        return self.files.filter(statut=FileAttente.Statut.EN_ATTENTE).count()


class FileAttente(models.Model):
    class Priorite(models.TextChoices):
        NORMALE = 'normale', 'Normale'
        URGENTE = 'urgente', 'Urgente'
        CRITIQUE = 'critique', 'Critique'

    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente'
        APPELE = 'appele', 'Appelé'
        TRAITE = 'traite', 'Traité'

    salle_attente = models.ForeignKey(SalleAttente, on_delete=models.CASCADE, related_name='files')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='files_attente')
    motif = models.CharField(max_length=255, blank=True)
    priorite = models.CharField(max_length=20, choices=Priorite.choices, default=Priorite.NORMALE)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE)
    heure_arrivee = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priorite', 'heure_arrivee']
        verbose_name = "File d'attente"
        verbose_name_plural = "Files d'attente"

    def __str__(self):
        return f"{self.patient} — {self.salle_attente.code}"
