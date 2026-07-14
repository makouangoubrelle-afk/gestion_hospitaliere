from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Infirmier(models.Model):
    class Service(models.TextChoices):
        URGENCES = 'urgences', 'Urgences'
        BLOC = 'bloc', 'Bloc opératoire'
        PEDIATRIE = 'pediatrie', 'Pédiatrie'
        MATERNITE = 'maternite', 'Maternité'
        REANIMATION = 'reanimation', 'Réanimation / Soins intensifs'
        HOSPITALISATION = 'hospitalisation', 'Hospitalisation générale'
        LABORATOIRE = 'laboratoire', 'Laboratoire'
        PHARMACIE = 'pharmacie', 'Pharmacie'

    class Grade(models.TextChoices):
        AS = 'as', 'Aide-soignant(e)'
        IDE = 'ide', 'Infirmier(ère) diplômé(e) d\'État'
        IADE = 'iade', 'IADE'
        CADRE = 'cadre', 'Cadre de santé'

    class Statut(models.TextChoices):
        ACTIF = 'active', 'Actif(ve)'
        INACTIF = 'inactive', 'Inactif(ve)'
        CONGE = 'on_leave', 'En congé'

    first_name = models.CharField(max_length=100, verbose_name='Prénom')
    last_name = models.CharField(max_length=100, verbose_name='Nom')
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
    )
    matricule = models.CharField(max_length=50, unique=True, verbose_name='Matricule')
    service = models.CharField(max_length=30, choices=Service.choices)
    grade = models.CharField(max_length=20, choices=Grade.choices, default=Grade.IDE)
    unite = models.CharField(max_length=100, blank=True, verbose_name='Unité / Service')
    shift = models.CharField(max_length=50, blank=True, verbose_name='Garde / Horaire')
    years_experience = models.PositiveIntegerField(default=0, verbose_name='Années d\'expérience')
    status = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Infirmier(ère)'
        verbose_name_plural = 'Infirmiers(ères)'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matricule})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
