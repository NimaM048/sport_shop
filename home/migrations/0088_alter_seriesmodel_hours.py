# Generated by Django 5.0.4 on 2024-08-19 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0087_activity_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seriesmodel',
            name='hours',
            field=models.IntegerField(blank=True, null=True, verbose_name='تعداد ساعت'),
        ),
    ]