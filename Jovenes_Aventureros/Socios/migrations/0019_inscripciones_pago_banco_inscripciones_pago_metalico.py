# Generated by Django 5.0.2 on 2024-07-27 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Socios', '0018_inscripcion_socio_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripciones',
            name='pago_banco',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inscripciones',
            name='pago_metalico',
            field=models.IntegerField(default=0),
        ),
    ]