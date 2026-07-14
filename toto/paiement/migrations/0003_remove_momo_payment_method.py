from django.db import migrations, models


def convert_momo_to_mtn(apps, schema_editor):
    Payment = apps.get_model('paiement', 'Payment')
    Payment.objects.filter(payment_method='momo').update(payment_method='mtn_momo')
    PaymentMethod = apps.get_model('paiement', 'PaymentMethod')
    PaymentMethod.objects.filter(gateway='momo').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('paiement', '0002_payment_methods_and_fields'),
    ]

    operations = [
        migrations.RunPython(convert_momo_to_mtn, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(
                choices=[
                    ('card', 'Carte bancaire'),
                    ('airtel_money', 'Airtel Mobile Money'),
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
            model_name='paymentmethod',
            name='gateway',
            field=models.CharField(
                choices=[
                    ('mtn_momo', 'MTN Mobile Money'),
                    ('airtel_money', 'Airtel Mobile Money'),
                    ('stripe', 'Carte bancaire (Stripe)'),
                    ('wave', 'Wave'),
                    ('orangemoney', 'Orange Money'),
                    ('local_bank', 'Banque locale'),
                ],
                max_length=50,
                unique=True,
            ),
        ),
    ]
