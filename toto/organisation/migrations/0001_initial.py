# Generated for SGHL

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medecins', '0001_initial'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalleAttente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('nom', models.CharField(max_length=120)),
                ('capacite', models.PositiveIntegerField(default=25)),
                ('zone', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': "Salle d'attente",
                'verbose_name_plural': "Salles d'attente",
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='SalleUrgence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('nom', models.CharField(max_length=120)),
                ('capacite', models.PositiveIntegerField(default=4)),
                ('statut', models.CharField(choices=[('libre', 'Libre'), ('occupee', 'Occupée'), ('maintenance', 'Maintenance')], default='libre', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('medecin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='salles_urgence', to='medecins.medecin')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='salles_urgence', to='patients.patient')),
            ],
            options={
                'verbose_name': "Salle d'urgence",
                'verbose_name_plural': "Salles d'urgence",
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='FileAttente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motif', models.CharField(blank=True, max_length=255)),
                ('priorite', models.CharField(choices=[('normale', 'Normale'), ('urgente', 'Urgente'), ('critique', 'Critique')], default='normale', max_length=20)),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('appele', 'Appelé'), ('traite', 'Traité')], default='en_attente', max_length=20)),
                ('heure_arrivee', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files_attente', to='patients.patient')),
                ('salle_attente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='organisation.salleattente')),
            ],
            options={
                'verbose_name': "File d'attente",
                'verbose_name_plural': "Files d'attente",
                'ordering': ['priorite', 'heure_arrivee'],
            },
        ),
    ]
