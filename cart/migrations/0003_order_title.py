# Generated by Django 5.0.4 on 2024-06-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='title',
            field=models.CharField(default='s', max_length=30),
        ),
    ]
