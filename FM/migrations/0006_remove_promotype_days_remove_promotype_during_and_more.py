# Generated by Django 5.0 on 2024-05-25 23:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FM', '0005_promotype_days_alter_promorequest_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotype',
            name='days',
        ),
        migrations.RemoveField(
            model_name='promotype',
            name='during',
        ),
        migrations.AddField(
            model_name='promotype',
            name='time_quantity',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='promotype',
            name='time_unit',
            field=models.CharField(choices=[('days', 'أيام'), ('hours', 'ساعات'), ('minutes', 'دقائق')], default='days', max_length=10),
        ),
        migrations.AlterField(
            model_name='promorequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
