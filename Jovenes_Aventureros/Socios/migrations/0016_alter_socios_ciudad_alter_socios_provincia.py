# Generated by Django 5.0.2 on 2024-07-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Socios', '0015_rename_apellido_socios_apellidos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socios',
            name='ciudad',
            field=models.CharField(default='Montilla', max_length=30),
        ),
        migrations.AlterField(
            model_name='socios',
            name='provincia',
            field=models.CharField(default='Córdoba', max_length=35),
        ),
    ]
