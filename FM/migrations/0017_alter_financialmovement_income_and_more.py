# Generated by Django 5.0.1 on 2024-05-29 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FM', '0016_financialreport_invested_projects_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialmovement',
            name='income',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='financialmovement',
            name='outcome',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
