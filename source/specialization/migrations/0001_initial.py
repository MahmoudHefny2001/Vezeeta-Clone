# Generated by Django 4.2.1 on 2023-08-21 01:46

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Specialization",
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
                    "specialization",
                    models.CharField(
                        choices=[
                            ("1", "جلدية"),
                            ("2", "اسنان"),
                            ("3", "نفسي"),
                            ("4", "عظام"),
                            ("5", "اطفال وحديثي الولادة"),
                            ("6", "مخ واعصاب"),
                            ("7", "نساءوتوليد"),
                            ("8", "انف واذن وحجره"),
                            ("9", "قلب واوعبة دموية"),
                            ("10", "أمراض الدم"),
                            ("11", "باطنة"),
                            ("12", "تخسيس وتغذية"),
                            ("13", "جراحة اطفال"),
                            ("14", "جراحة اورام"),
                            ("15", "جراحة اوعية دمويه"),
                            ("16", "جراحة تجميل"),
                            ("17", "جراحة سمنة وماظير"),
                            ("18", "جراحة عامة"),
                            ("19", "جراحة عمود فقري"),
                            ("20", "جراحة قلب وصدر"),
                            ("21", "جراحة مخ واعصاب"),
                            ("22", "حساسية ومناعة"),
                            ("23", "حقن مجهري واطفال انابيب"),
                            ("24", "ذكورة وعقم"),
                            ("25", "روماتيزم"),
                            ("26", "سمعيات"),
                            ("27", "صدر وجهاز تنفسي"),
                            ("28", "طب الاسرة"),
                            ("29", "طب تقويمي"),
                            ("30", "علاج الآلام"),
                            ("31", "علاج طبيعي واصابات ملاعب"),
                            ("32", "عيون"),
                            ("33", "كبد"),
                            ("34", "كلي"),
                            ("35", "مراكز اشعة"),
                            ("36", "مسالك بوليه"),
                            ("37", "ممارسة عامة"),
                            ("39", "نطق وتخاطب"),
                        ],
                        db_index=True,
                    ),
                ),
                (
                    "medical_speciality_description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
            ],
            options={
                "db_table": "specialization",
            },
        ),
    ]
