# Generated by Django 3.2 on 2022-01-09 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imaging_system_app', '0002_auto_20220109_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]