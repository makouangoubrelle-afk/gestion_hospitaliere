from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from medecins.models import Medecin
from patients.models import Patient


class Batiment(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bâtiment'

    def __str__(self):
        return self.nom


class ServiceHospitalier(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='services')
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('batiment', 'code')
        verbose_name = 'Service hospitalier'

    def __str__(self):
        return f"{self.nom} ({self.batiment.nom})"


class Chambre(models.Model):
    service = models.ForeignKey(ServiceHospitalier, on_delete=models.CASCADE, related_name='chambres')
    numero = models.CharField(max_length=20)
    etage = models.IntegerField(default=0)
    capacite = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('service', 'numero')
        verbose_name = 'Chambre'

    def __str__(self):
        return f"Chambre {self.numero} - {self.service.nom}"


class Lit(models.Model):
    class Statut(models.TextChoices):
        DISPONIBLE = 'disponible', 'Disponible'
        OCCUPE = 'occupe', 'Occupé'
        MAINTENANCE = 'maintenance', 'Maintenance'

    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='lits')
    numero = models.CharField(max_length=20)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.DISPONIBLE)
    patient_actuel = models.OneToOneField(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lit_actuel',
    )

    class Meta:
        unique_together = ('chambre', 'numero')
        verbose_name = 'Lit'

    def __str__(self):
        return f"Lit {self.numero} - {self.chambre}"

    def clean(self):
        if self.statut == self.Statut.OCCUPE and not self.patient_actuel:
            raise ValidationError('Un lit occupé doit avoir un patient assigné.')
        if self.statut == self.Statut.DISPONIBLE and self.patient_actuel:
            raise ValidationError('Un lit disponible ne peut pas avoir de patient.')


class Hospitalisation(models.Model):
    class Statut(models.TextChoices):
        ACTIVE = 'active', 'Active'
        TRANSFERT = 'transfert', 'En transfert'
        SORTIE = 'sortie', 'Sortie effectuée'
        ANNULEE = 'annulee', 'Annulée'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='hospitalisations')
    lit = models.ForeignKey(Lit, on_delete=models.PROTECT, related_name='hospitalisations')
    medecin_referent = models.ForeignKey(Medecin, on_delete=models.PROTECT, related_name='hospitalisations')
    date_entree = models.DateTimeField(default=timezone.now)
    date_sortie_prevue = models.DateField()
    date_sortie_effective = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIVE)
    motif = models.TextField()
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_entree']
        verbose_name = 'Hospitalisation'

    def __str__(self):
        return f"{self.patient} - {self.lit} ({self.statut})"

    def clean(self):
        if self.statut == self.Statut.ACTIVE:
            if self.lit.statut != Lit.Statut.DISPONIBLE and self.lit.patient_actuel not in (None, self.patient):
                raise ValidationError('Le lit sélectionné n\'est pas disponible.')
            if not self.date_sortie_prevue:
                raise ValidationError('La date prévisionnelle de sortie est obligatoire.')
            if not self.medecin_referent:
                raise ValidationError('Le médecin référent est obligatoire.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        if self.statut == self.Statut.ACTIVE:
            self.lit.statut = Lit.Statut.OCCUPE
            self.lit.patient_actuel = self.patient
            self.lit.save(update_fields=['statut', 'patient_actuel'])
            self.patient.status = 'active'
            self.patient.save(update_fields=['status'])

    def liberer_lit(self):
        self.lit.statut = Lit.Statut.DISPONIBLE
        self.lit.patient_actuel = None
        self.lit.save(update_fields=['statut', 'patient_actuel'])


class TransfertService(models.Model):
    hospitalisation = models.ForeignKey(Hospitalisation, on_delete=models.CASCADE, related_name='transferts')
    lit_source = models.ForeignKey(Lit, on_delete=models.PROTECT, related_name='transferts_sortants')
    lit_destination = models.ForeignKey(Lit, on_delete=models.PROTECT, related_name='transferts_entrants')
    date_transfert = models.DateTimeField(default=timezone.now)
    motif = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_transfert']
        verbose_name = 'Transfert inter-services'

    def __str__(self):
        return f"Transfert {self.hospitalisation.patient} -> {self.lit_destination}"


class ConstanteVitale(models.Model):
    hospitalisation = models.ForeignKey(Hospitalisation, on_delete=models.CASCADE, related_name='constantes')
    infirmier = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='constantes_saisies',
    )
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    tension_systolique = models.PositiveIntegerField(null=True, blank=True)
    tension_diastolique = models.PositiveIntegerField(null=True, blank=True)
    frequence_cardiaque = models.PositiveIntegerField(null=True, blank=True)
    saturation_o2 = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    mesure_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-mesure_at']
        verbose_name = 'Constante vitale'

    def __str__(self):
        return f"{self.hospitalisation.patient} - {self.mesure_at}"
