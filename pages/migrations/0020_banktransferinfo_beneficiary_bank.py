# Generated by Django 4.0.5 on 2022-07-05 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_consituentsdocs_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransferinfo',
            name='beneficiary_bank',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Beneficiary bank'),
        ),
    ]
