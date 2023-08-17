from django.db import models
from person.models import Person
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from .managers import DoctorManager

from person.validators import valid_phone_number

class Doctor(Person):
    base_role = Person.Role.DOCTOR

    class Meta:
        proxy = True

    objects = DoctorManager()


class DoctorExtended(Doctor):

    LOCATION_CHOICES = [
        ('1', "قنا"),
        ('2', "نجع-حمادي"),
        ('3', "الغردقة"),
        ('4', "أسيوط"),
        ('5', "المنيا"),
        ('6', "الأسكندرية"),
        ('7', "القاهرة"),
        ('8', "المنصورة"),
        ('9', "الزقازيق"),
        ('10', "المنوفية"),
        ('11', "الشرقية"),
        ('12', "الفيوم"),
        ('13', "البحيرة"),
        ('14', "الإسماعيلية"),
        ('15', "الجيزة"),
        ('16', "الدقهلية"),
        ('17', "السادس من أكتوبر"),
        ('18', "السويس"),
        ('19', "الشيخ زايد"),
        ('20', "العريش"),
        ('21', "الغربية"),
        ('22', "الفيوم"),
        ('23', "القليوبية"),
        ('24', "الوادي الجديد"),
        ('25', "بني سويف"),
        ('26', "بورسعيد"),
        ('27', "جنوب سيناء"),
        ('28', "دمياط"),
        ('29', "سوهاج"),
        ('30', "شمال سيناء"),
        ('31', "قنا"),
        ('32', "كفر الشيخ"),
        ('33', "مطروح"),
        ('34', "الأقصر"),
        ('35', "البحر الأحمر"),
        ('36', "السادات"),
        ('37', "السلام"),
        ('38', "العاشر من رمضان"),
        ('39', "العبور"),
        ('40', "العياط"),
        ('41', "القاهرة الجديدة"),
        ('42', "المحلة الكبرى"),
        ('43', "المرج"),
        ('44', "المطرية"),
        ('45', "المعادي"),
        ('46', "المنصورة"),
        ('47', "المنيا"),
        ('48', "النزهة"),
        ('49', "الهرم"),
        ('50', "بدر"),
        ('51', "بنها"),
        ('52', "بني سويف"),
        ('53', "بورسعيد"),
        ('54', "بولاق"),
        ('55', "تلا"),
        ('56', "تمي الأمديد"),
        ('57', "جرجا"),
        ('58', "دمنهور"),
        ('59', "رأس البر"),
        ('60', "زفتى"),
        ('61', "سوهاج"),
        ('62', "شبين الكوم"),
        ('63', "شبرا الخيمة")
    ]


    AREA_OR_CENTER_CHOICES = [
        ('1', "أبنوب"),
        ('2', "أسيوط"),
        ('3', "أسيوط الجديدة"),
        ('4', "أطفيح"),
        ('5', "البدرشين"),
        ('6', "البداري"),
        ('7', "البياضية"),
        ('8', "الحوامدية"),
        ('9', "الساحل"),
        ('10', "نجع حمادي"),
        ('11', "فرشوط"),
        ('12', "دشنا"),
        ('13', "قنا"),
        ('14', "قفط"),
        ('15', "قوص"),
        ('16', "نقادة")
    ]

    SPECIAIALIZATION_CHOICES = [
        ('1', "جلدية"),
        ('2', "اسنان"),
        ('3', "نفسي"),
        ('4', "عظام"),
        ('5', "اطفال وحديثي الولادة"),
        ('6', "مخ واعصاب"),
        ('7', "نساءوتوليد"),
        ('8', "انف واذن وحجره"),
        ('9', "قلب واوعبة دموية"),
        ('10', "أمراض الدم"),
        ('11', "باطنة"),
        ('12', "تخسيس وتغذية"),
        ('13', "جراحة اطفال"),
        ('14', "جراحة اورام"),
        ('15', "جراحة اوعية دمويه"),
        ('16', "جراحة تجميل"),
        ('17', "جراحة سمنة وماظير"),
        ('18', "جراحة عامة"),
        ('19', "جراحة عمود فقري"),
        ('20', "جراحة قلب وصدر"),
        ('21', "جراحة مخ واعصاب"),
        ('22', "حساسية ومناعة"),
        ('23', "حقن مجهري واطفال انابيب"),
        ('24', "ذكورة وعقم"),
        ('25', "روماتيزم"),
        ('26', "سمعيات"),
        ('27', "صدر وجهاز تنفسي"),
        ('28', "طب الاسرة"),
        ('29', "طب تقويمي"),
        ('30', "علاج الآلام"),
        ('31', "علاج طبيعي واصابات ملاعب"),
        ('32', "عيون"),
        ('33', "كبد"),
        ('34', "كلي"),
        ('35', "مراكز اشعة"),
        ('36', "مسالك بوليه"),
        ('37', "ممارسة عامة"),
        ('39', "نطق وتخاطب")
    ]         

    image = models.ImageField(upload_to="doctors/images", null=True, blank=True)
    

    full_name = models.CharField(max_length=100, null=False, blank=False)

    appointment_price = models.PositiveIntegerField(null=False, blank=False)

    medical_speciality_description = models.TextField(_("description"), null=True, blank=True)
    
    clinic_number = models.CharField(max_length=20, null=False, blank=False, unique=True, validators=[valid_phone_number])

    qualifications = models.TextField(null=False, blank=False)

    location = models.CharField(choices=LOCATION_CHOICES, null=False, blank=False)

    specialization = models.CharField(choices=SPECIAIALIZATION_CHOICES, null=False, blank=False, db_index=True)    

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

   
