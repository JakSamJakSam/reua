# Generated by Django 4.0.5 on 2022-07-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_remove_addresses_telegram_addresses_twitter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consituentsdocs',
            options={'ordering': ('order',), 'verbose_name': 'Установчий документ', 'verbose_name_plural': 'Установчи документи'},
        ),
        migrations.AddField(
            model_name='consituentsdocs',
            name='order',
            field=models.SmallIntegerField(default=1, verbose_name='Номер за порядком'),
            preserve_default=False,
        ),
    ]
