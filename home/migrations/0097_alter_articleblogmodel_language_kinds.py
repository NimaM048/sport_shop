# Generated by Django 5.0.4 on 2024-08-30 22:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0096_articleblogmodel_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleblogmodel',
            name='language_kinds',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogsss', to='home.category'),
        ),
    ]
