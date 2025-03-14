# Generated by Django 5.0 on 2023-12-29 23:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('The_Investor', '0003_investmentrequest'),
        ('The_Owner', '0002_projectcategory_project_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatInv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text1', models.TextField(blank=True, max_length=200, null=True)),
                ('date1', models.DateField()),
                ('text2', models.TextField(blank=True, max_length=200, null=True)),
                ('date2', models.DateField()),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('investor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='The_Investor.investor')),
            ],
        ),
        migrations.CreateModel(
            name='ChatOwn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text1', models.TextField(blank=True, max_length=200, null=True)),
                ('date1', models.DateField()),
                ('text2', models.TextField(blank=True, max_length=200, null=True)),
                ('date2', models.DateField()),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='The_Owner.owner')),
            ],
        ),
    ]
