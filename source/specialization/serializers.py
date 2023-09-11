from rest_framework import serializers
from .models import Specialization

from .choices import SPECIAIALIZATION_CHOICES


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        # fields = "__all__"
        exclude = ('id',)

    def get_specialization(self, obj):
        return dict(SPECIAIALIZATION_CHOICES).get(obj.specialization, '')
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialization'] = self.get_specialization(instance)
        return representation
    
    def update(self, instance, validated_data):
        instance.specialization = validated_data.get('specialization', instance.specialization)
        # medical_speciality_description is the previous value before the update
        # allow null for medical_speciality_description
        medical_speciality_description = validated_data.get('medical_speciality_description', None)
        if medical_speciality_description is not None:
            instance.medical_speciality_description = medical_speciality_description
        instance.save()
        return instance
    
    


class AvaliableSpecializationsSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    class Meta:
        model = Specialization
        fields = ("specialization", 'code',)

    
    def get_specialization(self, obj):
        return dict(SPECIAIALIZATION_CHOICES).get(obj.specialization, '')
    
    def get_code(self, obj):
        return obj.specialization

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialization'] = self.get_specialization(instance)
        return representation
    
    