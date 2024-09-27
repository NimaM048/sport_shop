# Generated by Django 5.0.4 on 2024-05-03 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_fullname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=11)),
                ('code', models.SmallIntegerField()),
                ('exprision_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]