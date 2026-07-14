# Generated manually for SGHL

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Infirmier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')])),
                ('matricule', models.CharField(max_length=50, unique=True, verbose_name='Matricule')),
                ('service', models.CharField(choices=[('urgences', 'Urgences'), ('bloc', 'Bloc opératoire'), ('pediatrie', 'Pédiatrie'), ('maternite', 'Maternité'), ('reanimation', 'Réanimation / Soins intensifs'), ('hospitalisation', 'Hospitalisation générale'), ('laboratoire', 'Laboratoire'), ('pharmacie', 'Pharmacie')], max_length=30)),
                ('grade', models.CharField(choices=[('as', 'Aide-soignant(e)'), ('ide', "Infirmier(ère) diplômé(e) d'État"), ('iade', 'IADE'), ('cadre', 'Cadre de santé')], default='ide', max_length=20)),
                ('unite', models.CharField(blank=True, max_length=100, verbose_name='Unité / Service')),
                ('shift', models.CharField(blank=True, max_length=50, verbose_name='Garde / Horaire')),
                ('years_experience', models.PositiveIntegerField(default=0, verbose_name="Années d'expérience")),
                ('status', models.CharField(choices=[('active', 'Actif(ve)'), ('inactive', 'Inactif(ve)'), ('on_leave', 'En congé')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Infirmier(ère)',
                'verbose_name_plural': 'Infirmiers(ères)',
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
