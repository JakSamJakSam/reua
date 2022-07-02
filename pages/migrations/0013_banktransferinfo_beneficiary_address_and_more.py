# Generated by Django 4.0.5 on 2022-07-02 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_banktransferinfo_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransferinfo',
            name='beneficiary_address',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='beneficiary address'),
        ),
        migrations.AddField(
            model_name='banktransferinfo',
            name='bic',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='beneficiary bic'),
        ),
        migrations.AddField(
            model_name='banktransferinfo',
            name='correspondent_bank_bic',
            field=models.CharField(blank=True, default=None, max_length=8, null=True, verbose_name='correspondent bank bic'),
        ),
        migrations.AddField(
            model_name='banktransferinfo',
            name='correspondent_bank_name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='correspondent bank name'),
        ),
        migrations.AlterField(
            model_name='banktransferinfo',
            name='bank',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Банк'),
        ),
        migrations.AlterField(
            model_name='banktransferinfo',
            name='edrpou',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Код за ЄДРПОУ'),
        ),
        migrations.AlterField(
            model_name='banktransferinfo',
            name='mfo',
            field=models.CharField(blank=True, default=None, max_length=6, null=True, verbose_name='МФО'),
        ),
    ]