# Generated by Django 5.0.4 on 2024-08-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0021_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
