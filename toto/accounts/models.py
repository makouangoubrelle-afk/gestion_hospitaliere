from django.conf import settings
from django.db import models


class Role(models.TextChoices):
    ADMIN = 'admin', 'Administrateur'
    MEDECIN = 'medecin', 'Médecin'
    INFIRMIER = 'infirmier', 'Infirmier(ère)'
    BIOLOGISTE = 'biologiste', 'Biologiste'
    PHARMACIEN = 'pharmacien', 'Pharmacien'
    COMPTABLE = 'comptable', 'Comptable'
    SECRETAIRE = 'secretaire', 'Secrétaire'
    PATIENT = 'patient', 'Patient'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT)
    phone = models.CharField(max_length=20, blank=True)
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_accounts',
    )
    medecin = models.ForeignKey(
        'medecins.Medecin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_accounts',
    )
    mfa_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class LoginJournal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='login_entries',
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Journal de connexion'

    def __str__(self):
        status = 'OK' if self.success else 'ECHEC'
        return f"{self.user.username} - {status} - {self.timestamp}"
