# Generated by Django 3.0.4 on 2020-04-04 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpayg',
            name='payg_end_hour',
            field=models.IntegerField(blank=True, verbose_name='従量変動終了時間(h)'),
        ),
    ]
