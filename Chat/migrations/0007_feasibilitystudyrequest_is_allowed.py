# Generated by Django 5.0.1 on 2024-06-02 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0006_delete_studytype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feasibilitystudyrequest',
            name='is_allowed',
            field=models.BooleanField(default=False),
        ),
    ]
