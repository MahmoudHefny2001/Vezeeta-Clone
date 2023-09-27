from django.http import JsonResponse
from rest_framework import serializers

import datetime

from .models import TimeSlot, DateSlot

from doctor.models import DoctorProfile



class TimeSlotSerializerForPatients(serializers.ModelSerializer):
    

    class Meta:
        model = TimeSlot    
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        try:
            representation['doctor_profile'] = {
                "doctor_id": instance.doctor_profile.doctor.id,
                "doctor_name": instance.doctor_profile.doctor.full_name,
                "doctor_specialization": instance.doctor_profile.doctor.specialization.specialization,
                "doctor_image": instance.doctor_profile.doctor.image,
            }        
        except Exception as e:
            raise "Image not found"
        finally:
            representation['doctor_profile'] = {
                "doctor_id": instance.doctor_profile.doctor.id,
                "doctor_name": instance.doctor_profile.doctor.full_name,
                "doctor_specialization": instance.doctor_profile.doctor.specialization.medical_speciality_description,
            }
        return representation    
    


class TimeSlotSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TimeSlot
        
        # fields = '__all__'
        # exclude = ('id', 'doctor_profile', )
        exclude = ('date',)



class DateSlotSerializer(serializers.ModelSerializer):
        time = TimeSlotSerializer(many=True, read_only=True)
        class Meta:
            model = DateSlot
            # fields = '__all__'
            exclude = ('is_reserved', 'doctor_profile')
            

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['time'] = TimeSlotSerializer(instance.time_slots.all(), many=True).data
            return representation
    



class TimeSlotSerializerForDoctors(serializers.ModelSerializer):
    
    class Meta:
        model = TimeSlot
        
        # fields = '__all__'
        exclude = ('doctor_profile', )

