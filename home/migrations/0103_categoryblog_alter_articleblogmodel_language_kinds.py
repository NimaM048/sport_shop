# Generated by Django 5.0.4 on 2024-09-03 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0102_counseling_button_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='عنوان دسته بندی را وارد کنید', max_length=100, null=True, verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(help_text='اسلاگ دسته بندی را وارد کنید', null=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی بلاگ ها',
            },
        ),
        migrations.AlterField(
            model_name='articleblogmodel',
            name='language_kinds',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_categories', to='home.categoryblog', verbose_name='زبان'),
        ),
    ]
