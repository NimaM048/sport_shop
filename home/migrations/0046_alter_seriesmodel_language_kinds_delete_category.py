# Generated by Django 5.0.4 on 2024-07-29 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_category_alter_seriesmodel_language_kinds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seriesmodel',
            name='language_kinds',
            field=models.CharField(max_length=30, null=True, verbose_name='زبان'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
