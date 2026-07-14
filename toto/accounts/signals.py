from django.contrib.auth.models import Group, User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import Role, UserProfile

ROLE_GROUPS = {
    Role.ADMIN: ['manage_users', 'view_dashboard', 'manage_hospitalisation', 'manage_laboratoire', 'manage_pharmacie', 'manage_facturation'],
    Role.MEDECIN: ['view_patients', 'manage_consultations', 'manage_prescriptions', 'view_hospitalisation'],
    Role.INFIRMIER: ['view_patients', 'manage_soins', 'view_hospitalisation'],
    Role.BIOLOGISTE: ['manage_laboratoire', 'validate_resultats'],
    Role.PHARMACIEN: ['manage_pharmacie', 'view_prescriptions'],
    Role.COMPTABLE: ['manage_facturation', 'view_dashboard'],
    Role.PATIENT: ['view_own_data', 'manage_rdv'],
}


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_migrate)
def setup_role_groups(sender, **kwargs):
    if sender.name != 'accounts':
        return
    for role, _label in Role.choices:
        Group.objects.get_or_create(name=role)
