# Generated by Django 3.2.18 on 2023-05-28 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0005_detallecotizacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cotizacion',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='cotizacion',
            name='precio',
        ),
    ]
