# Generated by Django 4.0.5 on 2022-07-20 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0024_alter_banktransferinfo_correspondent_bank_bic'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='paypalURL',
            field=models.URLField(blank=True, default=None, null=True, verbose_name="Адреса платіжної системи для 'PAYPAL'"),
        ),
    ]
