from rest_framework import serializers
from .models import Location, Address

from .choices import CITY_CHOICES, AREA_OR_CENTER_CHOICES 



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        # fields = "__all__"
        exclude = ('id',)

    
    def get_city(self, obj):
        return dict(CITY_CHOICES).get(obj.city, '')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['city'] = self.get_city(instance)
        return representation


class AddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Address
        # fields = "__all__"
        exclude = ('id',)


    def get_address(self, obj):
        return dict(AREA_OR_CENTER_CHOICES).get(obj.name, '')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = self.get_address(instance)
        return representation
    


class GeoAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = "__all__"
        exclude = ('id', 'location_details', 'location')


    def get_address(self, obj):
        return dict(AREA_OR_CENTER_CHOICES).get(obj.name, '')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = self.get_address(instance)
        return representation