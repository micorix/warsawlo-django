# Generated by Django 3.0.7 on 2021-04-16 20:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


def load_divisions(apps, schema_editor):
    School = apps.get_model("search", "School")
    for school in School.objects.iterator():
        if school.nickname is None:
            school.nickname = ""
        if school.data is None:
            school.data = {}
        if school.specialised_divisions:
            school.data["specialized_divisions"] = []
            for div in school.specialised_divisions:
                school.data["specialized_divisions"].append(div)
        school.save()


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0012_insert_profile_2020"),
    ]

    operations = [
        migrations.RunPython(load_divisions),
        migrations.RemoveField(
            model_name="school",
            name="school_type_generalised",
        ),
        migrations.RemoveField(
            model_name="school",
            name="specialised_divisions",
        ),
        migrations.AlterField(
            model_name="school",
            name="data",
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}, null=True),
        ),
        migrations.AlterField(
            model_name="school",
            name="school_type",
            field=models.CharField(
                choices=[
                    ("liceum ogólnokształcące", "Lo"),
                    ("technikum", "Tech"),
                    ("szkoła branżowa I stopnia", "Bran"),
                    ("szkoła specjalna przysposabiająca do pracy", "Spec"),
                    ("przedszkole", "Przed"),
                    ("szkoła podstawowa", "Sp"),
                    ("szkoła podstawowa artystyczna", "Spart"),
                    ("szkoła policealna", "Polic"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="school",
            name="student_type",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
