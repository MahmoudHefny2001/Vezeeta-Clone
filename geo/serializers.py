from rest_framework import serializers
from .models import City, AreaOrCenter


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"



class AreaOrCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOrCenter
        fields = "__all__"