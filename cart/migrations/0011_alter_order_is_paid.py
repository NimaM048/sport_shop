# Generated by Django 5.0.4 on 2024-07-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_order_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(),
        ),
    ]