from rest_framework import serializers
from .models import Location

from .choices import CITY_CHOICES

class LocationSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Location
        fields = "__all__"

    
    def get_city(self, obj):
        return dict(CITY_CHOICES).get(obj.city, '')

    # def get_area_or_center(self, obj):
    #     return dict(AREA_OR_CENTER_CHOICES).get(obj.area_or_center, '')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['area_or_center'] = self.get_area_or_center(instance)
        representation['city'] = self.get_city(instance)
        return representation


