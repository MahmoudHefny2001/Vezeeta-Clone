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
    image = models.ImageField(upload_to="doctors/images", null=True, blank=True)
    
    # first_name = models.CharField(max_length=150, null=False, blank=False)
    # last_name = models.CharField(max_length=150, null=False, blank=False)

    full_name = models.CharField(max_length=200, null=False, blank=False)

    appointment_price = models.PositiveIntegerField(null=False, blank=False)

    medical_speciality_description = models.TextField(_("description"), null=True, blank=True)

    # Specialization
    # specialization = models.ForeignKey(MedicalSpecialty, on_delete=models.PROTECT)

    qualifications = models.TextField(null=False, blank=False)


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

    location = models.CharField(choices=LOCATION_CHOICES, null=False, blank=False)

    location_details = models.TextField()
    

    SPECIAIALIZATION_CHOICES = [
        ("جلدية", "جلدية"),
        ("اسنان", "اسنان"),
        ("نفسي", "نفسي"),
        ("عظام", "عظام"),
        ("اطفال-وحديثي-الولادة", "اطفال وحديثي الولادة"),
        ("مخ-أعصاب", "مخ وأعصاب"),
        ("نسا-توليد", "نسا وتوليد"),
        ("أنف-أذن-حنجرة", "أنف وأذن وحنجرة"),
        ("قلب-أوعية", "قلب وأوعية دموية"),
        ("أمراض-دم", "أمراض دم"),
        ("باطنة", "باطنة"),
        ("تخسيس-تغذية", "تخسيس وتغذية"),
        ("جراحة-أطفال", "جراحة اطفال"),
        ("جراحة-أورام", "جراحة أورام"),
        
        # List all the next
        ("جراحة اطفال", "جراحة اطفال"),
        ("جراحة اورام", "جراحة اورام"),
        ("جراحة تجميل", "جراحة تجميل"),
        ("جراحة سمنة وماظير", "جراحة سمنة وماظير"),
        ("جراحة عامة",  "جراحة عامة"),

        ("جراحة عظام", "جراحة عظام"),   

        ("جراحة قلب وصدر", "جراحة قلب وصدر"),
        
        
        ("جراحة مخ واعصاب", "جراحة مخ واعصاب"),        
        ("جراحة نسائية", "جراحة نسائية"),
        ("حقن مجهري واطفال انابيب", "حقن مجهري واطفال انابيب"),
        ("داخلية", "داخلية"),
        ("روماتيزم ومفاصل", "روماتيزم ومفاصل"),
    

        # Add more specializations in arabic
        ("جراحة عامة", "جراحة عامة"),
        ("جراحة عظام", "جراحة عظام"),
        ("جراحة قلب وصدر", "جراحة قلب وصدر"),
        ("جراحة مخ واعصاب", "جراحة مخ واعصاب"),
        ("جراحة نسائية", "جراحة نسائية"),
        ("حقن مجهري واطفال انابيب", "حقن مجهري واطفال انابيب"),
        ("داخلية", "داخلية"),
        ("روماتيزم ومفاصل", "روماتيزم ومفاصل"),
        ("سمنة ومظاهر", "سمنة ومظاهر"),
        ("طب اسرة", "طب اسرة"),
        ("طب تقويمي", "طب تقويمي"),
        ("علاج طبيعي واصابات ملاعب", "علاج طبيعي واصابات ملاعب"),
        ("عيون", "عيون"),

        # List all the next
        ("أسنان", "أسنان"),
        ("أمراض الدم", "أمراض الدم"),
        ("أمراض القلب", "أمراض القلب"),
        ("أمراض الكلى", "أمراض الكلى"),
        ("أمراض النساء والتوليد", "أمراض النساء والتوليد"),
        ("أمراض النفسية", "أمراض النفسية"),
        ("أمراض باطنة", "أمراض باطنة"),
        ("أمراض تناسلية", "أمراض تناسلية"),

        # List all the next
        ("أمراض جلدية", "أمراض جلدية"),
        ("أمراض سمعية", "أمراض سمعية"),
        ("أمراض صدرية", "أمراض صدرية"),
        
        # List all the next
        # "روماتيزم" 
        # "سمعيات" 
        # "صدر وجهاز تنفسي"
        # "طب الاسرة"
        # "طب تقويمي" 
        # "علاج الآلام" 
        # "علاج طبيعي واصابات ملاعب"
        # "عيون" 
        # "كبد" 
        # "كلي" 

        ("أمراض قلب", "أمراض قلب"),
        ("أمراض معدية", "أمراض معدية"),
        ("أمراض وراثية", "أمراض وراثية"),
        ("أمراض وبائية", "أمراض وبائية"),
        ("أمراض وظائف تناسلية", "أمراض وظائف تناسلية"),
        ("أمراض وقاية", "أمراض وقاية"),
        

        ("مراكز اشعة", "مراكز اشعة"), 
        ("مسالك بولية", "مسالك بولية"),      
        ("ممارسة عامة", "ممارسة عامة"),
        ("نطق وتخاطب", "نطق وتخاطب"),
    ]

    specialization = models.CharField(choices=SPECIAIALIZATION_CHOICES, blank=True)    

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
   
