# Generated by Django 5.0.4 on 2024-07-28 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_alter_episode_duration_alter_episode_episode_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'verbose_name': 'اپیزود', 'verbose_name_plural': 'اپیزودها'},
        ),
    ]