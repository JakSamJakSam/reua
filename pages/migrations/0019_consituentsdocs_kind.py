# Generated by Django 4.0.5 on 2022-07-04 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_alter_consituentsdocs_options_consituentsdocs_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='consituentsdocs',
            name='kind',
            field=models.CharField(blank=True, choices=[('offer', 'Договір публичної оферти')], default=None, max_length=10, null=True, verbose_name='Вид файлу'),
        ),
    ]
