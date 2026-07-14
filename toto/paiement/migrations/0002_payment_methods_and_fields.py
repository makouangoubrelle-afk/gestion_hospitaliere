from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paiement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='card_last_four',
            field=models.CharField(blank=True, max_length=4, verbose_name='4 derniers chiffres carte'),
        ),
        migrations.AddField(
            model_name='payment',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='Téléphone Mobile Money'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(
                choices=[
                    ('momo', 'MoMo'),
                    ('card', 'Carte bancaire'),
                    ('airtel_money', 'Airtel Money'),
                    ('mtn_momo', 'MTN Mobile Money'),
                    ('cash', 'Espèces'),
                    ('transfer', 'Virement bancaire'),
                    ('check', 'Chèque'),
                    ('insurance', 'Assurance'),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'En attente'),
                    ('processed', 'Traité'),
                    ('completed', 'Confirmé'),
                    ('failed', 'Échoué'),
                    ('refunded', 'Remboursé'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='gateway',
            field=models.CharField(
                choices=[
                    ('momo', 'MoMo'),
                    ('mtn_momo', 'MTN Mobile Money'),
                    ('airtel_money', 'Airtel Money'),
                    ('stripe', 'Carte bancaire (Stripe)'),
                    ('wave', 'Wave'),
                    ('orangemoney', 'Orange Money'),
                    ('local_bank', 'Banque locale'),
                ],
                max_length=50,
                unique=True,
            ),
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-created_at'], 'verbose_name': 'Paiement', 'verbose_name_plural': 'Paiements'},
        ),
        migrations.AlterModelOptions(
            name='paymentmethod',
            options={'verbose_name': 'Passerelle de paiement', 'verbose_name_plural': 'Passerelles de paiement'},
        ),
    ]
