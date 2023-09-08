from rest_framework import serializers
from .models import Doctor, DoctorProfile, DoctorExtended
from patient.serializers import ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from review.serializers import ReviewSerializer
from review.models import Review

from geo.serializers import LocationSerializer, AddressSerializer
from specialization.serializers import SpecializationSerializer

from specialization.models import Specialization
from geo.models import Location, Address

from timeslot.serializers import TimeSlotSerializer

from timeslot.models import TimeSlot


class DoctorSerializer(serializers.ModelSerializer):
    
    specialization = SpecializationSerializer()
    address = AddressSerializer()

    password = serializers.CharField(write_only=True)

    class Meta:
        model = DoctorExtended
        fields = (
            "id",           
            "full_name",
            "image",
            "phone_number",
            "email",
            "qualifications",
            "password",
            "gender",
            "birth_date",
            "appointment_price" ,
            "clinic_number",
            "specialization",
            "address",
        )
        # extra_kwargs = {
            # 'birth_date': {'required': False},
        # }

    
    def create(self, validated_data):
        try:
            specialization_data = validated_data.pop("specialization")
            address_data = validated_data.pop('address')
            location_data = address_data.pop('location')

            location_instance, created = Location.objects.get_or_create(**location_data)
            address_instance = Address.objects.create(location=location_instance, **address_data)
            specialization_instance = Specialization.objects.create(**specialization_data)

            doctor = DoctorExtended.objects.create_user(
                address=address_instance, 
                specialization=specialization_instance, 
                **validated_data
            )
            return doctor
        except Exception as e:
            raise e



    def update(self, instance, validated_data):
        email = validated_data.get("email", None)
        phone_number = validated_data.get("phone_number", None)
        password = validated_data.get("password", None)
        
        if email is not None:
            instance.email = email
        if phone_number is not None:
            instance.phone_number = phone_number
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance




class OuterViewDoctorSerializer(serializers.ModelSerializer):    

    specialization = SpecializationSerializer()

    address = AddressSerializer()

    class Meta:
        model = DoctorExtended
        fields = (
            "id",
            "full_name",
            "image",
            "qualifications",
            "appointment_price" ,
            "address",
            "specialization",
            "clinic_number",
        )


class OuterViewDoctorProfileSerializer(serializers.ModelSerializer):

    doctor = OuterViewDoctorSerializer(read_only=True)

    availability = TimeSlotSerializer(many=True, read_only=True, allow_null=True, required=False)


    def get_availability_data(self, obj):
        time_slots = TimeSlot.objects.filter(doctor_profile=obj)
        time_slots_data = TimeSlotSerializer(time_slots, many=True).data
        return time_slots_data
    

    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        availability_data = self.get_availability_data(instance)
        representation['availability'] = availability_data
        return representation


    class Meta:
        model = DoctorProfile
        fields = ("id", "doctor", "availability",) 
        read_only_fields = ('doctor', 'availability', )


    
    def get_availability(self, obj):
        return obj.available_time_slots.all()



class DoctorProfileSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(read_only=True, many=True)
    doctor = OuterViewDoctorSerializer(read_only=True)
    
    availability = TimeSlotSerializer(many=True, allow_null=True, required=False)


    class Meta:
        model = DoctorProfile
        fields = '__all__'



class DoctorProfileSerializerForDoctors(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    # doctor = DoctorSerializerForDoctors(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = "__all__"

    def create(self, validated_data):
        doctor_profile = DoctorProfile.objects.create(**validated_data)
        return doctor_profile


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation



class DoctorProfileSerialzerForAppointmentDisplay(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        fields = "__all__"


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation



class AppointmentOuterViewDoctorProfileSerializer(serializers.ModelSerializer):
    doctor = OuterViewDoctorProfileSerializer(read_only=True)
    
    class Meta:
        model = DoctorProfile
        fields = "__all__"


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        return representation