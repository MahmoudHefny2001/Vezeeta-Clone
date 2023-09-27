# Generated by Django 4.2.1 on 2023-09-27 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("insurance", "0001_initial"),
        ("patient", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="medicalinsurance",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="patient.patientextended",
            ),
        ),
    ]
