# Generated by Django 5.0.4 on 2024-07-31 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_alter_seriesmodel_seseaons'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='footer',
            options={'verbose_name': 'پاورقی', 'verbose_name_plural': 'پاورقی ها'},
        ),
        migrations.RemoveField(
            model_name='footer',
            name='useful_links',
        ),
        migrations.RemoveField(
            model_name='footer',
            name='work_time',
        ),
        migrations.AddField(
            model_name='footer',
            name='address',
            field=models.TextField(blank=True, verbose_name='آدرس'),
        ),
        migrations.AddField(
            model_name='footer',
            name='copyright_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='سال کپی رایت'),
        ),
        migrations.AddField(
            model_name='footer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AddField(
            model_name='footer',
            name='show_social_media',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='نمایش شبکه های اجتماعی'),
        ),
        migrations.AddField(
            model_name='footer',
            name='social_media',
            field=models.JSONField(blank=True, null=True, verbose_name='شبکه های اجتماعی'),
        ),
        migrations.AddField(
            model_name='footer',
            name='working_hours',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ساعات کاری'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='about_us',
            field=models.TextField(verbose_name='درباره ما'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره تلفن'),
        ),
    ]
