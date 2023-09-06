# Generated by Django 4.2.1 on 2023-09-06 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("patient", "0002_initial"),
        ("timeslot", "0001_initial"),
        ("appointment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="patient_appointments",
                to="patient.patientextended",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="time_slot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="time_slots_appointments",
                to="timeslot.timeslot",
            ),
        ),
    ]
