from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from consultations.models import Consultation


class Medicament(models.Model):
    nom = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    forme = models.CharField(max_length=50, blank=True)
    dosage = models.CharField(max_length=50, blank=True)
    seuil_alerte = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Médicament'

    def __str__(self):
        return f"{self.nom} ({self.code})"

    @property
    def stock_total(self):
        return sum(lot.quantite for lot in self.lots.filter(quantite__gt=0))


class LotMedicament(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='lots')
    numero_lot = models.CharField(max_length=50)
    quantite = models.PositiveIntegerField(default=0)
    date_peremption = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('medicament', 'numero_lot')
        verbose_name = 'Lot médicament'

    def __str__(self):
        return f"{self.medicament.nom} - Lot {self.numero_lot}"

    @property
    def est_perime(self):
        return self.date_peremption < timezone.now().date()


class MouvementStock(models.Model):
    class TypeMouvement(models.TextChoices):
        ENTREE = 'entree', 'Entrée'
        SORTIE = 'sortie', 'Sortie'
        AJUSTEMENT = 'ajustement', 'Ajustement'

    lot = models.ForeignKey(LotMedicament, on_delete=models.PROTECT, related_name='mouvements')
    type_mouvement = models.CharField(max_length=20, choices=TypeMouvement.choices)
    quantite = models.PositiveIntegerField()
    motif = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mouvement de stock'

    def __str__(self):
        return f"{self.type_mouvement} - {self.quantite}"


class Prescription(models.Model):
    class Statut(models.TextChoices):
        BROUILLON = 'brouillon', 'Brouillon'
        VALIDEE = 'validee', 'Validée'
        ANNULEE = 'annulee', 'Annulée'

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions')
    medicament = models.ForeignKey(Medicament, on_delete=models.PROTECT)
    posologie = models.CharField(max_length=255)
    duree_jours = models.PositiveIntegerField(default=7)
    quantite = models.PositiveIntegerField(default=1)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.BROUILLON)
    validee_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Prescription'

    def __str__(self):
        return f"{self.medicament.nom} - {self.consultation}"

    def valider(self):
        if self.statut == self.Statut.VALIDEE:
            raise ValidationError('Prescription déjà validée et verrouillée.')
        self.statut = self.Statut.VALIDEE
        self.validee_at = timezone.now()
        self.save()
        self._decrementer_stock()

    def save(self, *args, **kwargs):
        if self.pk:
            original = Prescription.objects.filter(pk=self.pk).first()
            if original and original.statut == self.Statut.VALIDEE:
                raise ValidationError('Prescription verrouillée dès validation.')
        super().save(*args, **kwargs)

    def _decrementer_stock(self):
        lot = (
            self.medicament.lots.filter(quantite__gte=self.quantite)
            .order_by('date_peremption')
            .first()
        )
        if not lot:
            raise ValidationError('Stock insuffisant pour cette prescription.')
        lot.quantite -= self.quantite
        lot.save(update_fields=['quantite'])
        MouvementStock.objects.create(
            lot=lot,
            type_mouvement=MouvementStock.TypeMouvement.SORTIE,
            quantite=self.quantite,
            motif=f'Prescription #{self.pk}',
        )
