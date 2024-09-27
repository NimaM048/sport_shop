# Generated by Django 5.0.4 on 2024-04-26 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='آدرس ایمیل')),
                ('biography', models.TextField(blank=True, null=True)),
                ('fullname', models.CharField(max_length=50, verbose_name='نام کامل')),
                ('is_active', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='شماره تلفن')),
                ('is_admin', models.BooleanField(default=False, verbose_name='ادمین')),
                ('birthday_date', models.IntegerField()),
                ('web_site', models.CharField(max_length=100)),
                ('github', models.CharField(max_length=100)),
                ('linkdin', models.CharField(max_length=100)),
                ('telegram', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
    ]
