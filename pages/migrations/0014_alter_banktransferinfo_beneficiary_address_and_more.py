# Generated by Django 4.0.5 on 2022-07-02 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_banktransferinfo_beneficiary_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransferinfo',
            name='beneficiary_address',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Beneficiary address'),
        ),
        migrations.AlterField(
            model_name='banktransferinfo',
            name='bic',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Beneficiary bic'),
        ),
        migrations.AlterField(
            model_name='banktransferinfo',
            name='correspondent_bank_bic',
            field=models.CharField(blank=True, default=None, max_length=8, null=True, verbose_name='Correspondent bank bic'),
        ),
        migrations.AlterField(
            model_name='banktransferinfo',
            name='correspondent_bank_name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Correspondent bank name'),
        ),
    ]