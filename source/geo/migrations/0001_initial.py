# Generated by Django 4.2.1 on 2023-09-06 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Location",
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
                (
                    "city",
                    models.CharField(
                        choices=[
                            ("1", "المنيا"),
                            ("2", "قنا"),
                            ("3", "أسيوط"),
                            ("4", "سوهاج"),
                            ("5", "الغردقة"),
                            ("7", "القاهرة"),
                            ("6", "الأسكندرية"),
                            ("8", "المنصورة"),
                            ("11", "الشرقية"),
                            ("9", "الزقازيق"),
                            ("10", "المنوفية"),
                            ("11", "أسوان"),
                            ("12", "الفيوم"),
                            ("14", "الإسماعيلية"),
                            ("18", "السويس"),
                            ("19", "العريش"),
                            ("20", "الغربية"),
                            ("23", "الوادي الجديد"),
                            ("29", "شمال سيناء"),
                            ("33", "الأقصر"),
                            ("34", "البحر الأحمر"),
                        ],
                        db_index=True,
                    ),
                ),
            ],
            options={
                "db_table": "location",
            },
        ),
        migrations.CreateModel(
            name="Address",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("1", "أبنوب"),
                            ("2", "أسيوط"),
                            ("3", "أسيوط الجديدة"),
                            ("4", "أطفيح"),
                            ("5", "البدرشين"),
                            ("6", "البداري"),
                            ("7", "البياضية"),
                            ("8", "الحوامدية"),
                            ("9", "الساحل"),
                            ("10", "نجع حمادي"),
                            ("11", "فرشوط"),
                            ("12", "دشنا"),
                            ("13", "قنا"),
                            ("14", "قفط"),
                            ("15", "قوص"),
                            ("16", "نقادة"),
                            ("17", "مركز أبو تشت"),
                            ("18", "مركز فرشوط"),
                            ("19", "مركز نجع حمادي"),
                            ("20", "مركز الوقف"),
                            ("21", "مركز دشنا"),
                            ("22", "مركز قنا عاصمة المحافظة"),
                            ("26", "بني مر"),
                            ("27", "عرب العوامر"),
                            ("28", "الغنايم"),
                            ("29", "منفلوط"),
                            ("30", "بني حسين"),
                        ],
                        db_index=True,
                    ),
                ),
                ("location_details", models.TextField()),
                (
                    "location",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="geo.location",
                    ),
                ),
            ],
            options={
                "db_table": "address",
            },
        ),
    ]