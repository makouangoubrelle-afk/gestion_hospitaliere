from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    class ActionType(models.TextChoices):
        CREATE = 'CREATE', 'Création'
        UPDATE = 'UPDATE', 'Modification'
        DELETE = 'DELETE', 'Suppression'
        LOGIN = 'LOGIN', 'Connexion'
        LOGOUT = 'LOGOUT', 'Déconnexion'
        VALIDATE = 'VALIDATE', 'Validation'
        PUBLISH = 'PUBLISH', 'Publication'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
    )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Entrée audit trail'
        verbose_name_plural = 'Audit trail (livre-journal)'

    def __str__(self):
        return f"{self.action_type} - {self.model_name} - {self.timestamp}"
