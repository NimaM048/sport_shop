# Generated by Django 5.0.4 on 2024-08-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0075_alter_reply_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsectionmodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
