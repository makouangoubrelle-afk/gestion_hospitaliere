from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import Role, UserProfile


class Command(BaseCommand):
    help = 'Crée ou réinitialise les comptes de connexion SGHL'

    ACCOUNTS = [
        ('admin', 'admin1234', Role.ADMIN, 'admin@sghl.sn'),
        ('medecin', 'medecin1234', Role.MEDECIN, 'medecin@sghl.sn'),
        ('biologiste', 'bio1234', Role.BIOLOGISTE, 'bio@sghl.sn'),
        ('patient', 'patient1234', Role.PATIENT, 'patient@sghl.sn'),
        ('secretaire', 'secretaire1234', Role.SECRETAIRE, 'secretaire@sghl.sn'),
    ]

    def handle(self, *args, **options):
        for username, password, role, email in self.ACCOUNTS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'is_staff': username == 'admin', 'is_superuser': username == 'admin'},
            )
            user.set_password(password)
            user.is_active = True
            if username == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
            action = 'créé' if created else 'réinitialisé'
            self.stdout.write(f'  {username} — {action}')

        self.stdout.write(self.style.SUCCESS('Comptes prêts. Connexion : admin / admin1234'))
