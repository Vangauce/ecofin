# Generated by Django 3.2.18 on 2023-06-01 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='estado',
            field=models.CharField(default='Pendiente', max_length=50),
            preserve_default=False,
        ),
    ]
