# Generated manually for SGHL

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SiteLocalise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('type_lieu', models.CharField(choices=[('hopital', 'Hôpital'), ('clinique', 'Clinique'), ('urgences', 'Service des urgences'), ('laboratoire', 'Laboratoire'), ('pharmacie', 'Pharmacie'), ('ambulance', 'Ambulance / Mobile'), ('depistage', 'Centre de dépistage')], default='hopital', max_length=30)),
                ('adresse', models.TextField(blank=True)),
                ('ville', models.CharField(default='Dakar', max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site géolocalisé',
                'verbose_name_plural': 'Sites géolocalisés',
                'ordering': ['nom'],
            },
        ),
    ]
