# Generated by Django 5.0.4 on 2024-07-08 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_remove_order_series'),
        ('home', '0014_remove_seriesmodel_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='home.seriesmodel'),
        ),
    ]
