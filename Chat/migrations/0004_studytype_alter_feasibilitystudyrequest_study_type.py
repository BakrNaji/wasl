# Generated by Django 5.0.1 on 2024-06-02 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0003_feasibilitystudyrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='feasibilitystudyrequest',
            name='study_type',
            field=models.CharField(choices=[('market_analysis', 'تحليل السوق'), ('financial_analysis', 'التحليل المالي'), ('risk_assessment', 'تقييم المخاطر')], max_length=50),
        ),
    ]
