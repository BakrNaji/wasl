# Generated by Django 5.0.1 on 2024-05-30 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FM', '0018_rename_investmentrequest_financialmovement_investment_request_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialreport',
            name='promo_requests',
            field=models.ManyToManyField(related_name='financial_reports', to='FM.promorequest'),
        ),
    ]
