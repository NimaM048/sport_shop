# Generated by Django 5.0.4 on 2024-07-09 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_seriesmodel_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriesmodel',
            name='free',
            field=models.BooleanField(default=False),
        ),
    ]
