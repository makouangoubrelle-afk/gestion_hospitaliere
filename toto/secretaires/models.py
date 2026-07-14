from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Secretaire(models.Model):
    class Statut(models.TextChoices):
        ACTIF = 'active', 'Actif(ve)'
        INACTIF = 'inactive', 'Inactif(ve)'
        CONGE = 'on_leave', 'En congé'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
    )
    matricule = models.CharField(max_length=50, unique=True)
    bureau = models.CharField(max_length=100, blank=True, verbose_name='Bureau / Guichet')
    service_accueil = models.CharField(max_length=100, blank=True, verbose_name="Service d'accueil")
    horaires = models.CharField(max_length=100, blank=True, verbose_name='Horaires de permanence')
    status = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Secrétaire'
        verbose_name_plural = 'Secrétaires'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matricule})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
