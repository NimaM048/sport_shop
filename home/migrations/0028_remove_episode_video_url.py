# Generated by Django 5.0.4 on 2024-07-27 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_remove_seriesmodel_course_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='video_url',
        ),
    ]
