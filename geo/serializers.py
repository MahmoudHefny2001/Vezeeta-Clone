from rest_framework import serializers
from .models import Location, Area


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Area
        fields = '__all__'