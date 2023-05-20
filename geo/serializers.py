from rest_framework import serializers
from .models import Location, Area


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', )


class AreaSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Area
        fields = ('location', 'name')