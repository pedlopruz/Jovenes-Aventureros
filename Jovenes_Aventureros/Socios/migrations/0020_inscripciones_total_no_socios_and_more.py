# Generated by Django 5.0.2 on 2024-08-10 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Socios', '0019_inscripciones_pago_banco_inscripciones_pago_metalico'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripciones',
            name='total_no_socios',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inscripciones',
            name='total_socios',
            field=models.IntegerField(default=0),
        ),
    ]
