# Generated by Django 5.0.4 on 2024-08-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(max_length=50, verbose_name='نام کامل'),
        ),
    ]
