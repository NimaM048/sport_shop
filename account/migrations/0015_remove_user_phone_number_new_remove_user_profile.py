# Generated by Django 5.0.4 on 2024-08-10 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_user_phone_number_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_number_new',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
    ]
