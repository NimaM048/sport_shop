# Generated by Django 5.0.4 on 2024-07-27 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_rename_course_season_series_alter_season_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
