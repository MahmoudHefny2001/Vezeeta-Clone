# Generated by Django 4.2.1 on 2023-09-06 03:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("person", "0001_initial"),
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("person.person",),
        ),
        migrations.CreateModel(
            name="PatientExtended",
            fields=[
                (
                    "person_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255)),
                (
                    "has_medical_insurance",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
            ],
            options={
                "db_table": "patient",
            },
            bases=("patient.patient",),
        ),
        migrations.AddField(
            model_name="patientprofile",
            name="patient",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="patient.patientextended",
            ),
        ),
    ]
