# Generated by Django 5.0.2 on 2024-06-13 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Socios', '0003_socios_codigo_postal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socios',
            old_name='teléfono',
            new_name='telefono',
        ),
    ]
