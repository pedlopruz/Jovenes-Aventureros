# Generated by Django 5.0.2 on 2024-07-26 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Socios', '0016_alter_socios_ciudad_alter_socios_provincia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripciones',
            name='recaudacion_no_socios',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='inscripciones',
            name='recaudacion_socios',
            field=models.IntegerField(default=0),
        ),
    ]
