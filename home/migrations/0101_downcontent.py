# Generated by Django 5.0.4 on 2024-09-01 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0100_articleblogmodel_author_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'بخش پایین سایت',
            },
        ),
    ]
