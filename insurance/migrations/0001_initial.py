# Generated by Django 4.2.1 on 2023-07-31 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("medical_insurance_firm", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MedicalInsurance",
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
                ("full_name", models.CharField(max_length=200)),
                ("birth_date", models.DateField()),
                ("expiray_date", models.DateField()),
                (
                    "medical_insurance_number",
                    models.CharField(db_index=True, max_length=100, unique=True),
                ),
                (
                    "medical_insurance_image",
                    models.FileField(
                        blank=True, null=True, upload_to="patients/medical-inusrance/"
                    ),
                ),
                (
                    "medical_insurance_firm",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical_insurance_firm.firm",
                    ),
                ),
            ],
            options={
                "db_table": "medical_insurance",
            },
        ),
    ]
