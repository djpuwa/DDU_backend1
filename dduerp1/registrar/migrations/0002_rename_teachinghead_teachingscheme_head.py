# Generated by Django 4.0.2 on 2022-03-15 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachingscheme',
            old_name='teachingHead',
            new_name='head',
        ),
    ]
