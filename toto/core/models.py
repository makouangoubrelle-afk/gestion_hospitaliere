from django.db import models

from medecins.models import Medecin


class PlanningGarde(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='gardes')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    service = models.ForeignKey(
        'hospitalisation.ServiceHospitalier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gardes',
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_debut']
        verbose_name = 'Planning de garde'

    def __str__(self):
        return f"Garde {self.medecin} - {self.date_debut}"


class RendezVous(models.Model):
    class Statut(models.TextChoices):
        DEMANDE = 'demande', 'Demandé'
        CONFIRME = 'confirme', 'Confirmé'
        ANNULE = 'annule', 'Annulé'
        TERMINE = 'termine', 'Terminé'

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='rendez_vous')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='rendez_vous')
    date_rdv = models.DateTimeField()
    motif = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.DEMANDE)
    confirmation_email_envoyee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_rdv']
        verbose_name = 'Rendez-vous'

    def __str__(self):
        return f"RDV {self.patient} - {self.medecin} - {self.date_rdv}"
