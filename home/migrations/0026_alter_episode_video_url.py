# Generated by Django 5.0.4 on 2024-07-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_seriesmodel_course_category_seriesmodel_course_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='video_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
