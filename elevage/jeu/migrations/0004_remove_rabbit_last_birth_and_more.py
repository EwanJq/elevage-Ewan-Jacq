# Generated by Django 4.2 on 2025-04-15 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jeu', '0003_alter_rearing_rearing_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rabbit',
            name='last_birth',
        ),
        migrations.RemoveField(
            model_name='rabbit',
            name='pregnancy_duration',
        ),
    ]
