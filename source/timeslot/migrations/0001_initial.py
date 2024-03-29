# Generated by Django 4.2.1 on 2023-09-06 03:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("doctor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=datetime.date.today)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "is_reserved",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "doctor_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="available_time_slots",
                        to="doctor.doctorprofile",
                    ),
                ),
            ],
            options={
                "db_table": "time_slot",
            },
        ),
    ]
