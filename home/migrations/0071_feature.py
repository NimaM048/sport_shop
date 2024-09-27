# Generated by Django 5.0.4 on 2024-08-10 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0070_counseling'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='features')),
            ],
        ),
    ]
