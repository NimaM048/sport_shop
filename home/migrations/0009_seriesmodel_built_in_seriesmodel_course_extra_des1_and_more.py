# Generated by Django 5.0.4 on 2024-05-16 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_seriesmodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriesmodel',
            name='built_in',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seriesmodel',
            name='course_extra_des1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seriesmodel',
            name='course_extra_des2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seriesmodel',
            name='introdution_course',
            field=models.TextField(blank=True, null=True),
        ),
    ]
