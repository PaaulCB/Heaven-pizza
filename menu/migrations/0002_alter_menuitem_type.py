# Generated by Django 4.2.11 on 2024-04-09 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='type',
            field=models.CharField(choices=[('Starter', 'Starter'), ('Entree', 'Entree'), ('Dessert', 'Dessert'), ('Drink', 'Drink')], default='Starter', max_length=15),
        ),
    ]
