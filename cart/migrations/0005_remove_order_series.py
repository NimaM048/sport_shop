# Generated by Django 5.0.4 on 2024-06-29 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_order_title_order_series'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='series',
        ),
    ]
