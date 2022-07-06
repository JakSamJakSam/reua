# Generated by Django 4.0.5 on 2022-07-06 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_alter_financialreport_uploaded_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransferinfo',
            name='iban',
            field=models.CharField(blank=True, default=None, max_length=29, null=True, verbose_name='IBAN'),
        ),
        migrations.AlterField(
            model_name='banktransferinfo',
            name='bic',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Beneficiary (SWIFT)'),
        ),
    ]
