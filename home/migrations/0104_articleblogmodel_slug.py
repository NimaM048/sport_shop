# Generated by Django 5.0.4 on 2024-09-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0103_categoryblog_alter_articleblogmodel_language_kinds'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleblogmodel',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
