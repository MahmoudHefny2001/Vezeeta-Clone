# Generated by Django 4.2.1 on 2023-08-13 03:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctorextended",
            name="area_or_center",
            field=models.CharField(choices=[], default=""),
            preserve_default=False,
        ),
    ]