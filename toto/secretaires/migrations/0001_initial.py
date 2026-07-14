# Generated for SGHL

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Secretaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')])),
                ('matricule', models.CharField(max_length=50, unique=True)),
                ('bureau', models.CharField(blank=True, max_length=100, verbose_name='Bureau / Guichet')),
                ('service_accueil', models.CharField(blank=True, max_length=100, verbose_name="Service d'accueil")),
                ('horaires', models.CharField(blank=True, max_length=100, verbose_name='Horaires de permanence')),
                ('status', models.CharField(choices=[('active', 'Actif(ve)'), ('inactive', 'Inactif(ve)'), ('on_leave', 'En congé')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Secrétaire',
                'verbose_name_plural': 'Secrétaires',
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
