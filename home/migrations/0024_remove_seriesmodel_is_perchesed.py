# Generated by Django 5.0.4 on 2024-07-14 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_seriesmodel_is_perchesed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seriesmodel',
            name='is_perchesed',
        ),
    ]