# Generated by Django 4.0.5 on 2022-07-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0016_banktransferinfo_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresses',
            name='telegram',
        ),
        migrations.AddField(
            model_name='addresses',
            name='twitter',
            field=models.URLField(blank=True, default=None, null=True, verbose_name='Twitter'),
        ),
    ]