# Generated by Django 4.2.1 on 2023-08-14 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("geo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hospital",
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
                ("name", models.CharField(max_length=150)),
                ("phone", models.CharField(db_index=True, max_length=20, unique=True)),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="geo.location"
                    ),
                ),
            ],
            options={
                "db_table": "hospital",
            },
        ),
    ]
