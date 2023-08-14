# Generated by Django 4.2.1 on 2023-08-14 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("patient", "0002_initial"),
        ("appointment", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="patient.patientextended",
            ),
        ),
    ]
