# Generated by Django 5.0.1 on 2024-06-03 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0017_feasibilitystudy_feasibility_study_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
