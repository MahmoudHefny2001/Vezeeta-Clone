from django.db import models
from person.models import Person
from speciality.models import MedicalSpecialty
from clinic.models import Clinic
from geo.models import Location
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from .managers import DoctorManager


class Doctor(Person):
    base_role = Person.Role.DOCTOR

    class Meta:
        proxy = True

    objects = DoctorManager()


class DoctorExtended(Doctor):

    LOCATION_CHOICES = [
        ("قنا", "قنا"),
        ("نجع-حمادي", "نجع حمادي"),
        ("الغردقة", "الغردقة"),
        ("أسيوط", "أسيوط"),
        ("المنيا", "المنيا"),
        ("الأسكندرية", "الأسكندرية"),
        ("القاهرة", "القاهرة"),
        
        # Add more egyptian cities in arabic
        ("المنصورة", "المنصورة"),
        ("الزقازيق", "الزقازيق"),
        ("المنوفية", "المنوفية"),
        ("الشرقية", "الشرقية"),
        ("الفيوم", "الفيوم"),
        ("البحيرة", "البحيرة"),
        ("الإسماعيلية", "الإسماعيلية"),
        ("الجيزة", "الجيزة"),
        ("الدقهلية", "الدقهلية"),
        ("السادس من أكتوبر", "السادس من أكتوبر"),
        ("السويس", "السويس"),
        ("الشيخ زايد", "الشيخ زايد"),
        ("العريش", "العريش"),
        ("الغربية", "الغربية"),
        ("الفيوم", "الفيوم"),
        ("القليوبية", "القليوبية"),
        ("المنيا", "المنيا"),
        ("الوادي الجديد", "الوادي الجديد"),
        ("بني سويف", "بني سويف"),
        ("بورسعيد", "بورسعيد"),
        ("جنوب سيناء", "جنوب سيناء"),
        ("دمياط", "دمياط"),
        ("سوهاج", "سوهاج"),
        ("شمال سيناء", "شمال سيناء"),
        ("قنا", "قنا"),
        ("كفر الشيخ", "كفر الشيخ"),
        ("مطروح", "مطروح"),
        ("الأقصر", "الأقصر"),
        ("البحر الأحمر", "البحر الأحمر"),
        ("السادات", "السادات"),
        ("السلام", "السلام"),
        ("العاشر من رمضان", "العاشر من رمضان"),
        ("العبور", "العبور"),
        ("العياط", "العياط"),
        ("القاهرة الجديدة", "القاهرة الجديدة"),
        ("المحلة الكبرى", "المحلة الكبرى"),
        ("المرج", "المرج"),
        ("المطرية", "المطرية"),
        ("المعادي", "المعادي"),
        ("المنصورة", "المنصورة"),
        ("المنيا", "المنيا"),
        ("النزهة", "النزهة"),
        ("الهرم", "الهرم"),
        ("بدر", "بدر"),
        ("بنها", "بنها"),
        ("بني سويف", "بني سويف"),
        ("بورسعيد", "بورسعيد"),
        ("بولاق", "بولاق"),
        ("تلا", "تلا"),
        ("تمي الأمديد", "تمي الأمديد"),
        ("جرجا", "جرجا"),
        ("دمنهور", "دمنهور"),
        # list all 
        ("رأس البر", "رأس البر"),
        ("زفتى", "زفتى"),
        ("سوهاج", "سوهاج"),
        ("شبين الكوم", "شبين الكوم"),
        ("شبرا الخيمة", "شبرا الخيمة"),
    ]


    AREA_OR_CENTER_CHOICES = [
        # egyptian centers only 
        ("نجع حمادي", "نجع حمادي"),
        ("دشنا", "دشنا"),
        ("فرشوط", "فرشوط"),
        ("قنا", "قنا"),
        ("قفط", "قفط"),
        ("قوص", "قوص"),
        ("نقادة", "نقادة"),

        # Add assiut centers
        ("أبنوب", "أبنوب"),
        ("أسيوط", "أسيوط"),
        ("أسيوط الجديدة", "أسيوط الجديدة"),
        ("أطفيح", "أطفيح"),
        ("البدرشين", "البدرشين"),
        ("البداري", "البداري"),
        ("البياضية", "البياضية"),
        ("الحوامدية", "الحوامدية"),      
        ("الساحل", "الساحل"),

    ] 

    SPECIAIALIZATION_CHOICES = [
        ("1", "جلدية"),
        ("2", "اسنان"),
        ("3", "نفسي" ),
        ("4", "عظام" ),
        ("5", "اطفال وحديثي الولادة"),
        ("6", "مخ واعصاب "),
        ("7", "نساءوتوليد"),
        ("8", "انف واذن وحجره"),
        ("9", "قلب واوعبة دموية"),
        ("10", "أمراض الدم"),
        ("11", "باطنة"),
        ("12", "تخسيس وتغذية"),
        ("13", "جراحة اطفال" ),
        ("14", "جراحة اورام" ),
        ("15", "جراحة اوعية دمويه"),
        ("16", "جراحة تجميل"),
        ("17", "جراحة سمنة وماظير"),
        ("18", "جراحة عامة" ),
        ("19", "جراحة عمود فقري" ),
        ("20", "جراحة قلب وصدر" ),
        ("21", "جراحة مخ واعصاب"),
        ("22", "حساسية ومناعة" ),
        ("23", "حقن مجهري واطفال انابيب"),
        ("24", "ذكورة وعقم" ),
        ("25", "روماتيزم"),
        ("26", "سمعيات" ),
        ("27", "صدر وجهاز تنفسي"),
        ("28", "طب الاسرة"),
        ("29", "طب تقويمي"),
        ("30", "علاج الآلام"),
        ("31", "علاج طبيعي واصابات ملاعب"),
        ("32", "عيون"),
        ("33", "كبد" ),
        ("34", "كلي" ),
        ("35", "مراكز اشعة"),
        ("36", "مسالك بوليه"),
        ("37", "ممارسة عامة"),
        ("38", "نطق وتخاطب" )
    ]         

    image = models.ImageField(upload_to="doctors/images", null=True, blank=True)
    

    full_name = models.CharField(max_length=200, null=False, blank=False)

    appointment_price = models.PositiveIntegerField(null=False, blank=False)

    medical_speciality_description = models.TextField(_("description"), null=True, blank=True)

    clinic_number = models.CharField(max_length=20, null=True, blank=False)

    qualifications = models.TextField(null=False, blank=False)
    location = models.CharField(choices=LOCATION_CHOICES, null=False, blank=False)

    specialization = models.CharField(choices=SPECIAIALIZATION_CHOICES, blank=True)    

    area_or_center = models.CharField(choices=AREA_OR_CENTER_CHOICES, null=False, blank=False)

    location_details = models.TextField()

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        db_table = "doctor"


class DoctorProfile(models.Model):
    class Meta:
        db_table = "doctor_profile"

    doctor = models.OneToOneField(DoctorExtended, on_delete=models.CASCADE)


    # Clinic Information
    # clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)
   
