# Generated by Django 5.0.4 on 2024-09-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0101_downcontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='counseling',
            name='button_content',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]