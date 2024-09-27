# Generated by Django 5.0.4 on 2024-07-28 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_episode_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='duration',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='مدت زمان'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='episode_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='شماره اپیزود'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='home.season', verbose_name='فصل'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='videos/', verbose_name='فایل ویدئو'),
        ),
    ]
