# Generated by Django 5.0.4 on 2024-08-10 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0067_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounselingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='images/features/')),
            ],
        ),
    ]
