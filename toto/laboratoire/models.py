from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from consultations.models import Consultation
from hospitalisation.models import Hospitalisation
from patients.models import Patient


class TypeExamen(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Type d'examen"

    def __str__(self):
        return f"{self.code} - {self.nom}"


class CommandeLabo(models.Model):
    class Statut(models.TextChoices):
        COMMANDEE = 'commandee', 'Commandée'
        PRELEVEMENT = 'prelevement', 'Prélèvement effectué'
        AFFECTEE = 'affectee', 'Affectée'
        SAISIE = 'saisie', 'Résultats saisis'
        VALIDEE = 'validee', 'Validée'
        PUBLIEE = 'publiee', 'Publiée'
        ANNULEE = 'annulee', 'Annulée'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='commandes_labo')
    consultation = models.ForeignKey(Consultation, on_delete=models.SET_NULL, null=True, blank=True)
    hospitalisation = models.ForeignKey(Hospitalisation, on_delete=models.SET_NULL, null=True, blank=True)
    medecin_prescripteur = models.ForeignKey('medecins.Medecin', on_delete=models.PROTECT)
    type_examen = models.ForeignKey(TypeExamen, on_delete=models.PROTECT)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.COMMANDEE)
    numero_commande = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Commande laboratoire'

    def __str__(self):
        return self.numero_commande

    def clean(self):
        if not self.hospitalisation and not self.consultation:
            raise ValidationError('Une commande doit être liée à une consultation ou une hospitalisation active.')
        if self.hospitalisation and self.hospitalisation.statut != Hospitalisation.Statut.ACTIVE:
            raise ValidationError('Le traitement hospitalier dépend d\'une hospitalisation active.')


class Prelevement(models.Model):
    commande = models.OneToOneField(CommandeLabo, on_delete=models.CASCADE, related_name='prelevement')
    preleveur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_prelevement = models.DateTimeField(default=timezone.now)
    echantillon_id = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Prélèvement'

    def __str__(self):
        return self.echantillon_id


class ResultatLabo(models.Model):
    commande = models.OneToOneField(CommandeLabo, on_delete=models.CASCADE, related_name='resultat')
    valeur = models.TextField()
    unite = models.CharField(max_length=50, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    saisi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='resultats_saisis',
    )
    date_saisie = models.DateTimeField(default=timezone.now)
    valide = models.BooleanField(default=False)
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resultats_valides',
    )
    date_validation = models.DateTimeField(null=True, blank=True)
    publie = models.BooleanField(default=False)
    rapport_pdf = models.FileField(upload_to='labo/rapports/', blank=True, null=True)

    class Meta:
        verbose_name = 'Résultat laboratoire'

    def __str__(self):
        return f"Résultat {self.commande.numero_commande}"

    def valider(self, biologiste_user):
        profile = getattr(biologiste_user, 'profile', None)
        if not profile or profile.role != 'biologiste':
            raise ValidationError('Seul un biologiste peut valider un résultat.')
        if self.valide:
            raise ValidationError('Un résultat validé est immuable.')
        self.valide = True
        self.valide_par = biologiste_user
        self.date_validation = timezone.now()
        self.save()
        self.commande.statut = CommandeLabo.Statut.VALIDEE
        self.commande.save(update_fields=['statut', 'updated_at'])

    def save(self, *args, **kwargs):
        if self.pk:
            original = ResultatLabo.objects.filter(pk=self.pk).first()
            if original and original.valide:
                raise ValidationError('Un résultat validé est immuable.')
        super().save(*args, **kwargs)
