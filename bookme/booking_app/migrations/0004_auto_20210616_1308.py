# Generated by Django 3.1.2 on 2021-06-16 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0003_auto_20210614_1827'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='appointment',
            table='booking_app_appointment',
        ),
    ]