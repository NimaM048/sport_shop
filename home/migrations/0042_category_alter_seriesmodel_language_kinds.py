# Generated by Django 5.0.4 on 2024-07-29 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_alter_seriesmodel_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='seriesmodel',
            name='language_kinds',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='home.category', verbose_name='زبان'),
        ),
    ]
