# Generated by Django 5.0.4 on 2024-05-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_articleblogmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleblogmodel',
            name='article_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articleblogmodel',
            name='article_excerpt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articleblogmodel',
            name='article_extra_des1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articleblogmodel',
            name='article_extra_des2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articleblogmodel',
            name='built_in',
            field=models.TextField(blank=True, null=True),
        ),
    ]
