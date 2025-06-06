# Generated by Django 5.2.1 on 2025-05-30 00:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyreport',
            name='difference_percent',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='monthlyreport',
            name='report_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
