from rest_framework import serializers
from .models import Location, Address

from .choices import CITY_CHOICES, AREA_OR_CENTER_CHOICES 



class LocationSerializer(serializers.ModelSerializer):

    city = serializers.CharField()
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

    def update(self, instance, validated_data):
        
        city = validated_data.get("city", None)

        if city.isdigit():
            instance.city = city
            instance.save()
        else:
            print("city is not a digit")
            for key, value in CITY_CHOICES:
                if str(value) == str(city):
                    city = key
                    instance.city = city
                    instance.save()
                    
        return instance
    



class GeoLocationSerializer(serializers.ModelSerializer):

    code = serializers.SerializerMethodField()

    class Meta:
        model = Location
        # fields = "__all__"
        exclude = ('id',)


    def get_code(self, obj):
        # Loop through CITY_CHOICES to find the code corresponding to the city
        for value, display_text in CITY_CHOICES:
            if value == obj.city:
                return value
        return None  # Return None if not found in choices

    
    def get_city(self, obj):
        return dict(CITY_CHOICES).get(obj.city, '')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['city'] = self.get_city(instance)
        representation['code'] = self.get_code(instance)
        return representation


class AddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    name = serializers.CharField()

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
    

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        
        location_serializer = LocationSerializer(instance.location, data=location_data, partial=True)

        if location_serializer.is_valid():
            location_serializer.save()

        name = validated_data.get("name", None)
        location_details = validated_data.get("location_details", None)

        if location_details is not None:
            instance.location_details = location_details
            instance.save()

        if name.isdigit():
            instance.name = name
            instance.save()
        else:
            for key, value in AREA_OR_CENTER_CHOICES:
                if str(value) == str(name):
                    name = key
                    instance.name = name
                    instance.save()        
        
        return instance



class GeoAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = "__all__"
        exclude = ('id', 'location_details', 'location')


    def get_address(self, obj):
        return dict(AREA_OR_CENTER_CHOICES).get(obj.name, '')

    
    def get_location_code(self, obj):
        return obj.name

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = self.get_address(instance)
        representation['location'] = self.get_location_code(instance)
        return representation