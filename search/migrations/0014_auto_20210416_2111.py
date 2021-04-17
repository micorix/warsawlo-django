# Generated by Django 3.0.7 on 2021-04-16 21:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0013_auto_20210416_2059"),
    ]

    operations = [
        migrations.AlterField(
            model_name="school",
            name="data",
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="school",
            name="nickname",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]