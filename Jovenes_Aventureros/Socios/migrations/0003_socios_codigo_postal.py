# Generated by Django 5.0.2 on 2024-06-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Socios', '0002_alter_socios_numero_socio'),
    ]

    operations = [
        migrations.AddField(
            model_name='socios',
            name='codigo_postal',
            field=models.CharField(default=0, max_length=20),
        ),
    ]