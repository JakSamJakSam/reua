# Generated by Django 4.0.5 on 2022-06-28 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_banktransferinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Найменування (англ.)'),
        ),
    ]
