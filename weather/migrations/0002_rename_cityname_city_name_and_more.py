# Generated by Django 5.0.7 on 2024-08-08 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='cityName',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='usercity',
            old_name='cityName',
            new_name='city',
        ),
    ]
