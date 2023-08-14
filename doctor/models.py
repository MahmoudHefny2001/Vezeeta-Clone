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
        ("جلدية",  1),
        ("اسنان",  2),
        ("نفسي" ,  3),
        ("عظام" ,   4),
        ("اطفال وحديثي الولادة",   5),
        ("مخ واعصاب " ,  6),
        ("نساءوتوليد"    , 7),
        ("انف واذن وحجره", 8),
        ("قلب واوعبة دموية", 9),
        ("أمراض الدم", 10),
        ("باطنة", 11),
        ("تخسيس وتغذية", 12),
        ("جراحة اطفال", 13 ),
        ("جراحة اورام" , 14),
        ("جراحة اوعية دمويه", 15),
        ("جراحة تجميل", 16),
        ("جراحة سمنة وماظير", 17),
        ("جراحة عامة" , 18),
        ("جراحة عمود فقري", 19 ),
        ("جراحة قلب وصدر", 20 ),
        ("جراحة مخ واعصاب", 21),
        ("حساسية ومناعة" , 22),
        ("حقن مجهري واطفال انابيب", 23),
        ("ذكورة وعقم", 24 ),
        ("روماتيزم", 25),
        ("سمعيات" , 26),
        ("صدر وجهاز تنفسي", 27),
        ("طب الاسرة", 28),
        ("طب تقويمي", 29),
        ("علاج الآلام", 30),
        ("علاج طبيعي واصابات ملاعب", 31),
        ("عيون", 32),
        ("كبد" , 33),
        ("كلي" , 34),
        ("مراكز اشعة", 35),
        ("مسالك بوليه", 36),
        ("ممارسة عامة", 37),
        ("نطق وتخاطب", 39 )
    ]         

    image = models.ImageField(upload_to="doctors/images", null=True, blank=True)
    

    full_name = models.CharField(max_length=200, null=False, blank=False)

    appointment_price = models.PositiveIntegerField(null=False, blank=False)

    medical_speciality_description = models.TextField(_("description"), null=True, blank=True)

    clinic_number = models.CharField(max_length=20, null=True, blank=True)

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
   
