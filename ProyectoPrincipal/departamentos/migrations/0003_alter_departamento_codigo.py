# Generated by Django 4.0.4 on 2022-05-22 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0002_alter_departamento_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='codigo',
            field=models.IntegerField(null=True),
        ),
    ]
